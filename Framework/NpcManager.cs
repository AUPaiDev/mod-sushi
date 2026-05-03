using System.Collections.Generic;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;

namespace SuShiLegend.Framework
{
    public class NpcManager
    {
        private readonly IModHelper _helper;
        private readonly IMonitor _monitor;

        private static readonly Dictionary<string, NpcSpawnInfo> NpcDefinitions = new()
        {
            ["SuShi"] = new("Farm", new Vector2(64, 15), 2),
            ["Zhaoyun"] = new("Farm", new Vector2(66, 17), 2),
            ["Foyin"] = new("Farm", new Vector2(62, 17), 2)
        };

        public NpcManager(IModHelper helper, IMonitor monitor)
        {
            _helper = helper;
            _monitor = monitor;
        }

        public void SpawnAllNpcs()
        {
            foreach (var (name, info) in NpcDefinitions)
                SpawnNpc(name, info);
        }

        public void RemoveAllNpcs()
        {
            foreach (var (name, info) in NpcDefinitions)
            {
                var location = Game1.getLocationFromName(info.MapName);
                var npc = location?.getCharacterFromName(name);
                if (npc != null)
                    location.characters.Remove(npc);
            }
        }

        private void SpawnNpc(string name, NpcSpawnInfo info)
        {
            var location = Game1.getLocationFromName(info.MapName);
            if (location == null)
            {
                _monitor.Log($"Map {info.MapName} not found for {name}", LogLevel.Warn);
                return;
            }

            if (location.getCharacterFromName(name) != null)
                return;

            var sprite = new AnimatedSprite($"Characters/{name}", 0, 16, 32);
            Texture2D portrait = null;
            try
            {
                portrait = Game1.content.Load<Texture2D>($"Portraits/{name}");
            }
            catch
            {
                _monitor.Log($"Portrait not found for {name}, using null", LogLevel.Warn);
            }

            var npc = new NPC(
                sprite,
                info.Tile * 64f,
                info.FacingDirection,
                name
            );

            location.addCharacter(npc);
            _monitor.Log($"Spawned {name} at {info.MapName} ({info.Tile.X}, {info.Tile.Y})", LogLevel.Info);
        }

        public void SetDialogue(string npcName, string dialogue)
        {
            if (!NpcDefinitions.TryGetValue(npcName, out var info))
                return;

            var location = Game1.getLocationFromName(info.MapName);
            var npc = location?.getCharacterFromName(npcName);
            if (npc == null)
                return;

            npc.CurrentDialogue.Clear();
            npc.CurrentDialogue.Push(new Dialogue(npc, null, dialogue));
        }

        public NPC GetNpc(string name)
        {
            if (!NpcDefinitions.TryGetValue(name, out var info))
                return null;
            return Game1.getLocationFromName(info.MapName)?.getCharacterFromName(name);
        }

        public void OnAssetRequested(AssetRequestedEventArgs e)
        {
            foreach (var name in NpcDefinitions.Keys)
            {
                if (e.NameWithoutLocale.IsEquivalentTo($"Characters/{name}"))
                {
                    e.LoadFromModFile<Texture2D>($"assets/Characters/{name}.png", AssetLoadPriority.High);
                    return;
                }

                if (e.NameWithoutLocale.IsEquivalentTo($"Portraits/{name}"))
                {
                    e.LoadFromModFile<Texture2D>($"assets/Portraits/{name}.png", AssetLoadPriority.High);
                    return;
                }
            }
        }

        /// <summary>Expose NPC definitions so the wander manager can read spawn tiles.</summary>
        public static IReadOnlyDictionary<string, NpcSpawnInfo> Definitions => NpcDefinitions;

        public record NpcSpawnInfo(string MapName, Vector2 Tile, int FacingDirection);
    }
}
