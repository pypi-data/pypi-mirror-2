from itertools import chain, product

from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from zope.interface import implements

from bravo.blocks import blocks
from bravo.ibravo import IAutomaton, IDigHook
from bravo.utilities.automatic import naive_scan
from bravo.utilities.coords import adjust_coords_for_face
from bravo.utilities.spatial import Block2DSpatialDict, Block3DSpatialDict
from bravo.world import ChunkNotLoaded

from bravo.parameters import factory

FALLING = 0x8
"""
Flag indicating whether fluid is in freefall.
"""

class Fluid(object):
    """
    Fluid simulator.
    """

    implements(IAutomaton, IDigHook)

    sponge = None
    """
    Block that will soak up fluids and springs that are near it.

    Defaults to None, which effectively disables this feature.
    """

    def __init__(self):
        self.sponges = Block3DSpatialDict()
        self.springs = Block2DSpatialDict()

        self.tracked = set()
        self.new = set()

        self.loop = LoopingCall(self.process)

    def start(self):
        if not self.loop.running:
            self.loop.start(self.step)

    def stop(self):
        if self.loop.running:
            self.loop.stop()

    def schedule(self):
        if self.tracked:
            self.start()
        else:
            self.stop()

    @property
    def blocks(self):
        retval = [self.spring, self.fluid]
        if self.sponge:
            retval.append(self.sponge)
        return retval

    def feed(self, coordinates):
        """
        Accept the coordinates and stash them for later processing.
        """

        self.tracked.add(coordinates)
        self.schedule()

    scan = naive_scan

    def update_fluid(self, w, coords, falling, level=0):

        if not 0 <= coords[1] < 128:
            return False

        block = w.sync_get_block(coords)

        if (block in self.whitespace and not
            any(self.sponges.iteritemsnear(coords, 2))):
            w.sync_set_block(coords, self.fluid)
            if falling:
                level |= FALLING
            w.sync_set_metadata(coords, level)
            self.new.add(coords)
            return True
        return False

    def add_sponge(self, w, x, y, z):
        # Track this sponge.
        self.sponges[x, y, z] = True

        # Destroy the water! Destroy!
        for coords in product(
            xrange(x - 2, x + 3),
            xrange(max(y - 2, 0), min(y + 3, 128)),
            xrange(z - 2, z + 3),
            ):
            try:
                target = w.sync_get_block(coords)
                if target == self.spring:
                    if (coords[0], coords[2]) in self.springs:
                        del self.springs[coords[0],
                            coords[2]]
                    w.sync_destroy(coords)
                elif target == self.fluid:
                    w.sync_destroy(coords)
            except ChunkNotLoaded:
                pass

        # And now mark our surroundings so that they can be
        # updated appropriately.
        for coords in product(
            xrange(x - 3, x + 4),
            xrange(max(y - 3, 0), min(y + 4, 128)),
            xrange(z - 3, z + 4),
            ):
            if coords != (x, y, z):
                self.new.add(coords)

    def add_spring(self, w, x, y, z):
        # Double-check that we weren't placed inside a sponge. That's just
        # not going to work out.
        if any(self.sponges.iteritemsnear((x, y, z), 2)):
            w.sync_destroy((x, y, z))
            return

        # Track this spring.
        self.springs[x, z] = y

        # Neighbors on the xz-level.
        neighbors = ((x - 1, y, z), (x + 1, y, z), (x, y, z - 1),
            (x, y, z + 1))
        # Our downstairs pal.
        below = (x, y - 1, z)

        # Spawn water from springs.
        for coords in neighbors:
            try:
                self.update_fluid(w, coords, False)
            except ChunkNotLoaded:
                pass

        # Is this water falling down to the next y-level? We don't really
        # care, but we'll run the update nonetheless.
        self.update_fluid(w, below, True)

    def add_fluid(self, w, x, y, z):
        # Neighbors on the xz-level.
        neighbors = ((x - 1, y, z), (x + 1, y, z), (x, y, z - 1),
                (x, y, z + 1))
        # Our downstairs pal.
        below = (x, y - 1, z)

        # Double-check that we weren't placed inside a sponge.
        if any(self.sponges.iteritemsnear((x, y, z), 2)):
            w.sync_destroy((x, y, z))
            return

        # First, figure out whether or not we should be spreading.  Let's see
        # if there are any springs nearby which are above us and thus able to
        # fuel us.
        if not any(springy >= y
            for springy in
            self.springs.itervaluesnear((x, z), self.levels + 1)):
            # Oh noes, we're drying up! We should mark our neighbors and dry
            # ourselves up.
            self.new.update(neighbors)
            self.new.add(below)
            w.sync_destroy((x, y, z))
            return

        newmd = self.levels + 1

        for coords in neighbors:
            try:
                jones = w.sync_get_block(coords)
                if jones == self.spring:
                    newmd = 0
                    self.new.update(neighbors)
                    break
                elif jones == self.fluid:
                    jonesmd = w.sync_get_metadata(coords) & ~FALLING
                    if jonesmd + 1 < newmd:
                        newmd = jonesmd + 1
            except ChunkNotLoaded:
                pass

        current_md = w.sync_get_metadata((x,y,z))
        if newmd > self.levels and current_md < FALLING:
            # We should dry up.
            self.new.update(neighbors)
            self.new.add(below)
            w.sync_destroy((x, y, z))
            return

        # Mark any neighbors which should adjust themselves. This will only
        # mark lower water levels than ourselves, and only if they are
        # definitely too low.
        for coords in neighbors:
            try:
                neighbor = w.sync_get_metadata(coords)
                if neighbor & ~FALLING > newmd + 1:
                    self.new.add(coords)
            except ChunkNotLoaded:
                pass

        # Now, it's time to extend water. Remember, either the water flows
        # downward to the next y-level, or it flows out across the xz-level,
        # but *not* both.

        # Fall down to the next y-level, if possible.
        if self.update_fluid(w, below, True, newmd):
            return

        # Clamp our newmd and assign. Also, set ourselves again; we changed
        # this time and we might change again.
        if current_md < FALLING:
            w.sync_set_metadata((x, y, z), newmd)

        # If pending block is already above fluid, don't keep spreading.
        if neighbor == self.fluid:
            return

        # Otherwise, just fill our neighbors with water, where applicable, and
        # mark them.
        if newmd < self.levels:
            newmd += 1
            for coords in neighbors:
                try:
                    self.update_fluid(w, coords, False, newmd)
                except ChunkNotLoaded:
                    pass

    def remove_sponge(self, x, y, z):
        # The evil sponge tyrant is gone. Flow, minions, flow!
        for coords in product(xrange(x - 3, x + 4),
            xrange(max(y - 3, 0), min(y + 4, 128)), xrange(z - 3, z + 4)):
            if coords != (x, y, z):
                self.new.add(coords)

    def remove_spring(self, x, y, z):
        # Neighbors on the xz-level.
        neighbors = ((x - 1, y, z), (x + 1, y, z), (x, y, z - 1),
                (x, y, z + 1))
        # Our downstairs pal.
        below = (x, y - 1, z)

        # Destroyed spring. Add neighbors and below to blocks to update.
        del self.springs[x, z]

        self.new.update(neighbors)
        self.new.add(below)

    def process(self):
        w = factory.world

        for x, y, z in self.tracked:
            # Try each block separately. If it can't be done, it'll be
            # discarded from the set simply by not being added to the new set
            # for the next iteration.
            try:
                block = w.sync_get_block((x, y, z))
                if block == self.sponge:
                    self.add_sponge(w, x, y, z)
                elif block == self.spring:
                    self.add_spring(w, x, y, z)
                elif block == self.fluid:
                    self.add_fluid(w, x, y, z)
                else:
                    # Hm, why would a pending block not be any of the things we
                    # care about? Maybe it used to be a spring or something?
                    if (x, z) in self.springs:
                        self.remove_spring(x, y, z)
                    elif (x, y, z) in self.sponges:
                        self.remove_sponge(x, y, z)
            except ChunkNotLoaded:
                pass

        # Flush affected chunks.
        to_flush = set()
        for x, y, z in chain(self.tracked, self.new):
            to_flush.add((x // 16, z // 16))
        for x, z in to_flush:
            d = factory.world.request_chunk(x, z)
            d.addCallback(factory.flush_chunk)

        self.tracked = self.new
        self.new = set()

        # Prune, and reschedule.
        self.schedule()

    @inlineCallbacks
    def dig_hook(self, chunk, x, y, z, block):
        """
        Check for neighboring water that might want to spread.

        Also check to see whether we are, for example, dug ice that has turned
        back into water.
        """

        x += chunk.x * 16
        z += chunk.z * 16

        # Check for sponges first, since they will mark the entirety of the
        # area.
        if block == self.sponge:
            for coords in product(
                xrange(x - 3, x + 4),
                xrange(max(y - 3, 0), min(y + 4, 128)),
                xrange(z - 3, z + 4),
                ):
                self.tracked.add(coords)

        else:
            for (dx, dy, dz) in (
                ( 0, 0,  0),
                ( 0, 0,  1),
                ( 0, 0, -1),
                ( 0, 1,  0),
                ( 1, 0,  0),
                (-1, 0,  0)):
                coords = x + dx, y + dy, z + dz
                test_block = yield factory.world.get_block(coords)
                if test_block in (self.spring, self.fluid):
                    self.tracked.add(coords)

        self.schedule()

    before = ("build",)
    after = tuple()

class Water(Fluid):

    spring = blocks["spring"].slot
    fluid = blocks["water"].slot
    levels = 7

    sponge = blocks["sponge"].slot

    whitespace = (blocks["air"].slot, blocks["snow"].slot)
    meltables = (blocks["ice"].slot,)

    step = 0.2

    name = "water"

class Lava(Fluid):

    spring = blocks["lava-spring"].slot
    fluid = blocks["lava"].slot
    levels = 3

    whitespace = (blocks["air"].slot, blocks["snow"].slot)
    meltables = (blocks["ice"].slot,)

    step = 0.5

    name = "lava"

class Redstone(object):

    implements(IAutomaton, IDigHook)

    step = 0.2

    blocks = (blocks["redstone-wire"].slot,)

    def __init__(self):
        self.tracked = set()
        self.powered = set()

        self.loop = LoopingCall(self.process)

    def start(self):
        if not self.loop.running:
            self.loop.start(self.step)

    def stop(self):
        if self.loop.running:
            self.loop.stop()

    def schedule(self):
        if self.tracked:
            self.start()
        else:
            self.stop()

    def update_wires(self, x, y, z, enabled):
        """
        Trace the wires starting at a certain point, and either enable or
        disable them.
        """

        level = 0xf if enabled else 0x0
        traveled = set()
        traveling = set([(x, y, z)])

        while traveling:
            # Visit nodes.
            for coords in traveling:
                metadata = factory.world.sync_get_metadata(coords)
                if metadata != level:
                    factory.world.set_metadata(coords, level)
                    traveled.add(coords)

            # Rotate the nodes from last time into the old list, generate the
            # new list again, and then do a difference update to avoid
            # visiting previously touched nodes.
            nodes = [(
                (i - 1, j, k    ),
                (i + 1, j, k    ),
                (i,     j, k - 1),
                (i,     j, k + 1))
                for (i, j, k) in traveling]
            traveling.clear()
            for l in nodes:
                for coords in l:
                    block = factory.world.sync_get_block(coords)
                    if block == blocks["redstone-wire"].slot:
                        traveling.add(coords)
            traveling.difference_update(traveled)

            if level:
                level -= 1

    def update_powered_block(self, x, y, z, enabled):
        """
        Update a powered non-redstone block.
        """

        neighbors = ((x - 1, y, z), (x + 1, y, z), (x, y, z - 1),
            (x, y, z + 1))

        affected = []

        for neighbor in neighbors:
            block = factory.world.sync_get_block(neighbor)
            if block == blocks["redstone-wire"].slot:
                args = neighbor + (enabled,)
                self.update_wires(*args)
            elif block == blocks["redstone-torch"].slot and enabled:
                metadata = factory.world.sync_get_metadata(neighbor)
                face = blocks["redstone-torch"].face(metadata)
                target = adjust_coords_for_face(neighbor, face)
                if target == (x, y, z):
                    # We should turn off this torch.
                    factory.world.sync_set_block(neighbor,
                        blocks["redstone-torch-off"].slot)
                    affected.append(neighbor)

        return affected

    def run_circuit(self, x, y, z):
        """
        Iterate through a circuit, starting at the given block, and return a
        list of circuits which have been affected.
        """

        world = factory.world
        block = factory.world.sync_get_block((x, y, z))
        neighbors = ((x - 1, y, z), (x + 1, y, z), (x, y, z - 1),
            (x, y, z + 1))

        affected = set()

        if block == blocks["lever"].slot:
            # Power/depower the block the lever is attached to.
            metadata = factory.world.sync_get_metadata((x, y, z))
            powered = metadata & 0x8
            face = blocks["lever"].face(metadata & ~0x8)
            target = adjust_coords_for_face((x, y, z), face)

            if powered:
                self.powered.add(target)
            else:
                self.powered.discard(target)

            affected.add(target)

        else:
            # Let's update anything around us.
            l = self.update_powered_block(x, y, z, (x, y, z) in self.powered)
            affected.update(l)

        if block == blocks["redstone-torch"].slot:
            # Turn on neighboring wires, as appropriate.
            for coords in neighbors:
                if (world.get_block(coords) ==
                    blocks["redstone-wire"].slot):
                    self.update_wires(factory, coords[0], coords[1],
                        coords[2], True)

        if block == blocks["redstone-torch-off"].slot:
            # Turn off neighboring wires, as appropriate.
            for coords in neighbors:
                if (world.get_block(coords) ==
                    blocks["redstone-wire"].slot):
                    self.update_wires(factory, coords[0], coords[1],
                        coords[2], False)

        elif block == blocks["redstone-wire"].slot:
            # Get wire status from neighbors.
            if any(world.get_block(coords) ==
                blocks["redstone-torch"].slot
                for coords in neighbors):
                # We should probably be lit.
                self.update_wires(factory, x, y, z, True)
            else:
                # Find the strongest neighboring wire, and use that.
                new_level = max(factory.world.get_metadata(coords)
                    for coords in neighbors
                    if factory.world.get_block(coords) ==
                        blocks["redstone-wire"].slot)
                if new_level > 0x0:
                    new_level -= 1
                world.set_metadata((x, y, z), new_level)

        return affected

    def process(self):
        pass

    @inlineCallbacks
    def feed(self, coords):

        self.tracked.add(coords)

        # Wire wants state updates from its neighbors.
        block = yield factory.world.get_block(coords)
        if block == blocks["redstone-wire"].slot:
            x, y, z = coords
            self.tracked.update(((x - 1, y, z), (x + 1, y, z), (x, y, z - 1),
                (x, y, z + 1)))

    scan = naive_scan

    def dig_hook(self, chunk, x, y, z, block):
        pass

    name = "redstone"

    before = ("build",)
    after = tuple()

water = Water()
lava = Lava()
redstone = Redstone()
