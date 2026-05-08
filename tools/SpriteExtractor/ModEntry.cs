using System;
using System.IO;
using Microsoft.Xna.Framework.Graphics;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;

namespace SpriteExtractor
{
    public class ModEntry : Mod
    {
        public override void Entry(IModHelper helper)
        {
            helper.Events.GameLoop.SaveLoaded += OnSaveLoaded;
            helper.Events.Input.ButtonPressed += OnButtonPressed;
        }

        private void OnSaveLoaded(object sender, SaveLoadedEventArgs e)
        {
            ExtractSprites();
        }

        private void OnButtonPressed(object sender, ButtonPressedEventArgs e)
        {
            if (e.Button == SButton.F8)
                ExtractSprites();
        }

        private void ExtractSprites()
        {
            string outputDir = Path.Combine(Helper.DirectoryPath, "output");
            Directory.CreateDirectory(outputDir);

            string[] npcs = { "Abigail", "Sebastian", "Sam", "Harvey", "Elliott", "Shane",
                              "Haley", "Leah", "Maru", "Penny", "Emily", "Alex" };

            foreach (string npc in npcs)
            {
                try
                {
                    // Extract character sprite sheet
                    Texture2D charTex = Helper.GameContent.Load<Texture2D>($"Characters/{npc}");
                    SaveTexture(charTex, Path.Combine(outputDir, $"Characters_{npc}.png"));
                    Monitor.Log($"Extracted Characters/{npc}: {charTex.Width}x{charTex.Height}", LogLevel.Info);

                    // Extract portrait
                    Texture2D portTex = Helper.GameContent.Load<Texture2D>($"Portraits/{npc}");
                    SaveTexture(portTex, Path.Combine(outputDir, $"Portraits_{npc}.png"));
                    Monitor.Log($"Extracted Portraits/{npc}: {portTex.Width}x{portTex.Height}", LogLevel.Info);
                }
                catch (Exception ex)
                {
                    Monitor.Log($"Failed to extract {npc}: {ex.Message}", LogLevel.Warn);
                }
            }

            Monitor.Log($"Sprites extracted to: {outputDir}", LogLevel.Alert);
        }

        private void SaveTexture(Texture2D texture, string path)
        {
            using (var stream = File.Create(path))
            {
                texture.SaveAsPng(stream, texture.Width, texture.Height);
            }
        }
    }
}
