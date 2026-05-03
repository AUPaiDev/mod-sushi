using System;
using System.Collections.Generic;
using Microsoft.Xna.Framework;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;
using SuShiLegend.Framework;

namespace SuShiLegend
{
    public class ModEntry : Mod
    {
        public static ModEntry Instance { get; private set; }

        private NpcManager _npcManager;
        private QuestManager _questManager;
        private NpcWanderManager _wanderManager;
        private ModData _data;
        private Dictionary<string, string> _dialogues;

        public override void Entry(IModHelper helper)
        {
            Instance = this;
            _npcManager = new NpcManager(helper, Monitor);
            _questManager = new QuestManager(helper, Monitor);
            _wanderManager = new NpcWanderManager(Monitor);
            LoadDialogues();

            helper.Events.GameLoop.SaveLoaded += OnSaveLoaded;
            helper.Events.GameLoop.Saving += OnSaving;
            helper.Events.GameLoop.DayStarted += OnDayStarted;
            helper.Events.GameLoop.TimeChanged += OnTimeChanged;
            helper.Events.GameLoop.UpdateTicked += OnUpdateTicked;
            helper.Events.Input.ButtonPressed += OnButtonPressed;
            helper.Events.Content.AssetRequested += OnAssetRequested;

            Monitor.Log("西湖遗梦 已加载", LogLevel.Info);
        }

        private void LoadDialogues()
        {
            try
            {
                _dialogues = Helper.ModContent.Load<Dictionary<string, string>>("assets/i18n/default.json");
            }
            catch (Exception ex)
            {
                Monitor.Log($"Failed to load dialogues: {ex.Message}", LogLevel.Error);
                _dialogues = new Dictionary<string, string>();
            }
        }

        private string GetDialogue(string key)
        {
            return _dialogues.TryGetValue(key, out var text) ? text : $"[Missing: {key}]";
        }

        private void OnSaveLoaded(object sender, SaveLoadedEventArgs e)
        {
            _data = Helper.Data.ReadSaveData<ModData>("SuShiLegend.SaveData") ?? new ModData();
            Monitor.Log("Save data loaded", LogLevel.Debug);
        }

        private void OnSaving(object sender, SavingEventArgs e)
        {
            _wanderManager.Clear();
            _npcManager.RemoveAllNpcs();
            if (_data != null)
                Helper.Data.WriteSaveData("SuShiLegend.SaveData", _data);
        }

        private void OnDayStarted(object sender, DayStartedEventArgs e)
        {
            if (!Context.IsWorldReady || _data == null)
                return;

            _npcManager.SpawnAllNpcs();
            RefreshAllDialogues();

            // Register all NPCs for wandering near their spawn points
            _wanderManager.Clear();
            foreach (var (name, info) in NpcManager.Definitions)
                _wanderManager.Register(name, info.Tile);

            if (!_data.StoneTabletFound)
            {
                _data.StoneTabletFound = true;
                Game1.addHUDMessage(new HUDMessage(
                    "你感到一股古老的力量在星露谷中苏醒...三道光影飞向了不同的方向。", 2));
            }
        }

        private void OnUpdateTicked(object sender, UpdateTickedEventArgs e)
        {
            if (!Context.IsWorldReady)
                return;

            _wanderManager.Update(_npcManager);
        }

        private void RefreshAllDialogues()
        {
            RefreshSuShiDialogue();
            RefreshZhaoyunDialogue();
            RefreshFoyinDialogue();
        }

        private void RefreshSuShiDialogue()
        {
            var state = _data.NpcStates["SuShi"];
            string dialogue = state.DialogueStage switch
            {
                0 => GetDialogue("SuShi.Intro"),
                1 => GetDialogue("SuShi.Working"),
                2 => GetDialogue("SuShi.Working"),
                3 => GetDialogue("SuShi.Quest2Done"),
                _ => GetSeasonalDialogue("SuShi")
            };
            _npcManager.SetDialogue("SuShi", dialogue);
        }

        private void RefreshZhaoyunDialogue()
        {
            var state = _data.NpcStates["Zhaoyun"];
            string dialogue = state.DialogueStage switch
            {
                0 => GetDialogue("Zhaoyun.Intro"),
                1 => GetDialogue("Zhaoyun.Working"),
                2 => GetDialogue("Zhaoyun.Done"),
                _ => GetSeasonalDialogue("Zhaoyun")
            };
            _npcManager.SetDialogue("Zhaoyun", dialogue);
        }

        private void RefreshFoyinDialogue()
        {
            var state = _data.NpcStates["Foyin"];
            string dialogue = _data.FoyinRiddleProgress switch
            {
                0 => state.DialogueStage == 0 ? GetDialogue("Foyin.Intro") : GetDialogue("Foyin.Riddle1"),
                1 => GetDialogue("Foyin.Riddle2"),
                2 => GetDialogue("Foyin.Riddle3"),
                _ => GetDialogue("Foyin.Done")
            };
            _npcManager.SetDialogue("Foyin", dialogue);
        }

        private string GetSeasonalDialogue(string npcName)
        {
            string season = Game1.currentSeason;
            string seasonKey = season switch
            {
                "spring" => "Spring",
                "summer" => "Summer",
                "fall" => "Fall",
                "winter" => "Winter",
                _ => "Spring"
            };

            if (Game1.isRaining && _dialogues.ContainsKey($"{npcName}.Rain"))
                return GetDialogue($"{npcName}.Rain");

            string key = $"{npcName}.{seasonKey}";
            return _dialogues.ContainsKey(key) ? GetDialogue(key) : GetDialogue($"{npcName}.Intro");
        }

        private void OnTimeChanged(object sender, TimeChangedEventArgs e)
        {
            if (!Context.IsWorldReady || _data == null)
                return;

            _questManager.CheckQuestProgress(_data, _npcManager);
            CheckPoetryPageDiscovery();
        }

        private void CheckPoetryPageDiscovery()
        {
            if (!_data.ActiveQuests.Contains(QuestManager.QuestPoetry))
                return;
            if (_data.PoetryPagesFound >= 3)
                return;

            string locationName = Game1.currentLocation?.Name;
            bool found = _data.PoetryPagesFound switch
            {
                0 => locationName == "UndergroundMine",
                1 => locationName == "Forest",
                2 => locationName == "Beach",
                _ => false
            };

            if (!found)
                return;

            _data.PoetryPagesFound++;
            string[] pageKeys = { "Zhaoyun.Page1", "Zhaoyun.Page2", "Zhaoyun.AllPages" };
            string dialogueKey = pageKeys[_data.PoetryPagesFound - 1];
            Game1.addHUDMessage(new HUDMessage($"发现了诗词残页！（{_data.PoetryPagesFound}/3）", 2));

            if (_data.PoetryPagesFound >= 3)
            {
                _questManager.CompleteQuest(QuestManager.QuestPoetry, _data);
                Game1.player.Money += 3000;
                _data.NpcStates["Zhaoyun"].DialogueStage = 2;
                _npcManager.SetDialogue("Zhaoyun", GetDialogue("Zhaoyun.AllPages"));
            }
        }

        private void OnButtonPressed(object sender, ButtonPressedEventArgs e)
        {
            if (!Context.IsWorldReady || _data == null)
                return;

            if (!e.Button.IsActionButton())
                return;

            var playerTile = Game1.player.Tile;
            var facingOffset = Game1.player.FacingDirection switch
            {
                0 => new Vector2(0, -1),
                1 => new Vector2(1, 0),
                2 => new Vector2(0, 1),
                3 => new Vector2(-1, 0),
                _ => Vector2.Zero
            };
            var targetTile = playerTile + facingOffset;

            var npc = Game1.currentLocation?.isCharacterAtTile(targetTile);
            if (npc == null)
                return;

            HandleNpcInteraction(npc.Name);
        }

        private void HandleNpcInteraction(string npcName)
        {
            switch (npcName)
            {
                case "SuShi":
                    HandleSuShiInteraction();
                    break;
                case "Zhaoyun":
                    HandleZhaoyunInteraction();
                    break;
                case "Foyin":
                    HandleFoyinInteraction();
                    break;
            }
        }

        private void HandleSuShiInteraction()
        {
            var state = _data.NpcStates["SuShi"];
            if (state.DialogueStage == 0)
            {
                state.DialogueStage = 1;
                _questManager.StartQuest(QuestManager.QuestCauseway, _data);
                _npcManager.SetDialogue("SuShi", GetDialogue("SuShi.Quest1"));
            }
        }

        private void HandleZhaoyunInteraction()
        {
            var state = _data.NpcStates["Zhaoyun"];
            if (state.DialogueStage == 0)
            {
                state.DialogueStage = 1;
                _questManager.StartQuest(QuestManager.QuestPoetry, _data);
                _npcManager.SetDialogue("Zhaoyun", GetDialogue("Zhaoyun.Quest"));
            }
        }

        private void HandleFoyinInteraction()
        {
            var state = _data.NpcStates["Foyin"];
            if (state.DialogueStage == 0)
            {
                state.DialogueStage = 1;
                _questManager.StartQuest(QuestManager.QuestZen, _data);
            }

            if (_data.FoyinRiddleProgress < 3 && _data.ActiveQuests.Contains(QuestManager.QuestZen))
            {
                _data.FoyinRiddleProgress++;
                string answerKey = $"Foyin.Riddle{_data.FoyinRiddleProgress}.Answer";
                _npcManager.SetDialogue("Foyin", GetDialogue(answerKey));

                if (_data.FoyinRiddleProgress >= 3)
                {
                    _questManager.CompleteQuest(QuestManager.QuestZen, _data);
                    // +2 luck for 3 days
                    var buff = new Buff("tauwoo.SuShi.ZenMind",
                        duration: 43200, // 3 in-game days (3 * 14400 ticks)
                        displayName: "禅心",
                        description: "佛印禅师的祝福，内心平静，运气+2。");
                    buff.effects.LuckLevel.Value = 2;
                    Game1.player.applyBuff(buff);
                    Game1.addHUDMessage(new HUDMessage("获得增益：禅心（运气+2，持续3天）", 2));
                }
            }
        }

        private void OnAssetRequested(object sender, AssetRequestedEventArgs e)
        {
            _npcManager.OnAssetRequested(e);
            _questManager.OnAssetRequested(e);
        }
    }
}