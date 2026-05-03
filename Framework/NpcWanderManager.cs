using System;
using System.Collections.Generic;
using Microsoft.Xna.Framework;
using StardewModdingAPI;
using StardewValley;
using StardewValley.Pathfinding;

namespace SuShiLegend.Framework
{
    /// <summary>
    /// Makes custom NPCs wander randomly near their spawn point.
    /// Each NPC picks a random walkable tile within a radius and pathfinds to it.
    /// When they arrive (or fail), they idle briefly, then pick a new target.
    /// </summary>
    public class NpcWanderManager
    {
        private readonly IMonitor _monitor;
        private readonly Random _rng = new();

        /// How far (in tiles) an NPC can wander from its home position.
        private const int WanderRadius = 4;

        /// Min/max idle ticks between wander moves (60 ticks ≈ 1 second).
        private const int MinIdleTicks = 120;  // ~2 seconds
        private const int MaxIdleTicks = 360;  // ~6 seconds

        private readonly Dictionary<string, WanderState> _states = new();

        public NpcWanderManager(IMonitor monitor)
        {
            _monitor = monitor;
        }

        /// <summary>Register an NPC for wandering around its current tile.</summary>
        public void Register(string npcName, Vector2 homeTile)
        {
            _states[npcName] = new WanderState
            {
                HomeTile = homeTile,
                IdleTicksRemaining = _rng.Next(MinIdleTicks, MaxIdleTicks),
                IsMoving = false
            };
        }

        /// <summary>Unregister all NPCs (call on save/day end).</summary>
        public void Clear()
        {
            _states.Clear();
        }

        /// <summary>Call every tick (UpdateTicked) to drive wander behavior.</summary>
        public void Update(NpcManager npcManager)
        {
            foreach (var (name, state) in _states)
            {
                var npc = npcManager.GetNpc(name);
                if (npc == null)
                    continue;

                // If NPC is currently pathfinding, check if done
                if (state.IsMoving)
                {
                    if (npc.controller == null)
                    {
                        // Arrived or path was cancelled
                        state.IsMoving = false;
                        state.IdleTicksRemaining = _rng.Next(MinIdleTicks, MaxIdleTicks);
                    }
                    continue;
                }

                // Idle countdown
                state.IdleTicksRemaining--;
                if (state.IdleTicksRemaining > 0)
                    continue;

                // Pick a random nearby tile and try to pathfind there
                TryWander(npc, state);
            }
        }

        private void TryWander(NPC npc, WanderState state)
        {
            var location = npc.currentLocation;
            if (location == null)
            {
                state.IdleTicksRemaining = MaxIdleTicks;
                return;
            }

            // Try up to 8 random tiles to find a walkable one
            for (int attempt = 0; attempt < 8; attempt++)
            {
                int dx = _rng.Next(-WanderRadius, WanderRadius + 1);
                int dy = _rng.Next(-WanderRadius, WanderRadius + 1);

                // Stay within radius (circular)
                if (dx * dx + dy * dy > WanderRadius * WanderRadius)
                    continue;

                int targetX = (int)state.HomeTile.X + dx;
                int targetY = (int)state.HomeTile.Y + dy;

                // Check if tile is passable
                if (!IsTileWalkable(location, targetX, targetY))
                    continue;

                // Don't pathfind to current tile
                var npcTile = npc.TilePoint;
                if (npcTile.X == targetX && npcTile.Y == targetY)
                    continue;

                // Set up pathfinding
                try
                {
                    npc.controller = new PathFindController(
                        npc,
                        location,
                        new Point(targetX, targetY),
                        _rng.Next(4) // random facing direction on arrival
                    );

                    if (npc.controller.pathToEndPoint != null && npc.controller.pathToEndPoint.Count > 0)
                    {
                        state.IsMoving = true;
                        return;
                    }
                    else
                    {
                        // Pathfinding failed, try another tile
                        npc.controller = null;
                    }
                }
                catch
                {
                    npc.controller = null;
                }
            }

            // All attempts failed, wait and try again later
            state.IdleTicksRemaining = _rng.Next(MinIdleTicks, MaxIdleTicks);
        }

        private static bool IsTileWalkable(GameLocation location, int x, int y)
        {
            var tileLocation = new Vector2(x, y);
            // Basic bounds check; PathFindController handles detailed passability
            return location.isTileOnMap(tileLocation)
                && !location.IsTileOccupiedBy(tileLocation);
        }

        private class WanderState
        {
            public Vector2 HomeTile;
            public int IdleTicksRemaining;
            public bool IsMoving;
        }
    }
}
