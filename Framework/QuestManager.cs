using System.Collections.Generic;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;
using StardewValley.Quests;

namespace SuShiLegend.Framework
{
    public class QuestManager
    {
        private readonly IModHelper _helper;
        private readonly IMonitor _monitor;

        public const string QuestCauseway = "tauwoo.SuShi.Causeway";
        public const string QuestDongpo = "tauwoo.SuShi.DongpoRou";
        public const string QuestPoetry = "tauwoo.SuShi.Poetry";
        public const string QuestZen = "tauwoo.SuShi.Zen";

        private static readonly Dictionary<string, string> QuestData = new()
        {
            [QuestCauseway] = string.Join("/", new[]
            {
                "Basic",                                          // type
                "星露堤",                                          // title
                "苏轼希望在星露谷修建一条堤坝，重现西湖苏堤的美景。他需要200块石头和100根木材。", // description
                "收集 200 石头和 100 木材交给苏轼。",                  // objective
                "null",                                           // trigger
                QuestDongpo,                                      // next quest
                "5000",                                           // reward money
                "true",                                           // canBeCancelled
                "null"                                            // reaction text
            }),
            [QuestDongpo] = string.Join("/", new[]
            {
                "Basic",
                "东坡肉",
                "苏轼想要烹制他最拿手的东坡肉，需要你带来食材：一块猪肉、酱油和糖。",
                "带猪肉、酱油和糖给苏轼。",
                "null",
                "null",
                "2000",
                "true",
                "null"
            }),
            [QuestPoetry] = string.Join("/", new[]
            {
                "Basic",
                "水调歌头",
                "朝云正在寻找散落在星露谷各处的诗词残页，希望将苏轼的名作《水调歌头》重新拼凑完整。",
                "在矿洞、森林和海滩各找到一页诗词残页。",
                "null",
                "null",
                "3000",
                "true",
                "null"
            }),
            [QuestZen] = string.Join("/", new[]
            {
                "Basic",
                "禅意问答",
                "佛印禅师想用三个禅意谜语考验你的智慧。回答正确将获得禅心的祝福。",
                "回答佛印的三个禅意谜语。",
                "null",
                "null",
                "0",
                "true",
                "null"
            })
        };

        public QuestManager(IModHelper helper, IMonitor monitor)
        {
            _helper = helper;
            _monitor = monitor;
        }

        public void OnAssetRequested(AssetRequestedEventArgs e)
        {
            if (!e.Name.IsEquivalentTo("Data/Quests"))
                return;

            e.Edit(asset =>
            {
                var data = asset.AsDictionary<string, string>().Data;
                foreach (var (id, questString) in QuestData)
                    data[id] = questString;
            });
        }

        public void StartQuest(string questId, ModData modData)
        {
            if (modData.ActiveQuests.Contains(questId) || modData.CompletedQuests.Contains(questId))
                return;

            Game1.player.addQuest(questId);
            modData.ActiveQuests.Add(questId);
            _monitor.Log($"Quest started: {questId}", LogLevel.Info);
        }

        public void CompleteQuest(string questId, ModData modData)
        {
            if (!modData.ActiveQuests.Contains(questId))
                return;

            Game1.player.completeQuest(questId);
            modData.ActiveQuests.Remove(questId);
            modData.CompletedQuests.Add(questId);
            _monitor.Log($"Quest completed: {questId}", LogLevel.Info);
        }

        public void CheckQuestProgress(ModData modData, NpcManager npcManager)
        {
            if (modData.ActiveQuests.Contains(QuestCauseway))
                CheckCausewayQuest(modData, npcManager);

            if (modData.ActiveQuests.Contains(QuestDongpo))
                CheckDongpoQuest(modData, npcManager);

            CheckAllQuestsComplete(modData);
        }

        private void CheckCausewayQuest(ModData modData, NpcManager npcManager)
        {
            int stone = Game1.player.Items.CountId("(O)390", int.MaxValue);
            int wood = Game1.player.Items.CountId("(O)388", int.MaxValue);

            if (stone >= 200 && wood >= 100)
            {
                Game1.player.Items.ReduceId("(O)390", 200);
                Game1.player.Items.ReduceId("(O)388", 100);
                CompleteQuest(QuestCauseway, modData);
                Game1.player.Money += 5000;
                npcManager.SetDialogue("SuShi",
                    "太好了！有了这些材料，星露堤很快就能建成。$h#$b#" +
                    "想当年在杭州，我也是这样带领百姓疏浚西湖、修筑苏堤的。$s#$b#" +
                    "来，尝尝我的拿手菜——东坡肉如何？我还需要一些食材...");
                modData.NpcStates["SuShi"].DialogueStage = 2;
                StartQuest(QuestDongpo, modData);
            }
        }

        private void CheckDongpoQuest(ModData modData, NpcManager npcManager)
        {
            bool hasPork = Game1.player.Items.CountId("(O)184", int.MaxValue) >= 1;
            bool hasOil = Game1.player.Items.CountId("(O)247", int.MaxValue) >= 1;
            bool hasSugar = Game1.player.Items.CountId("(O)245", int.MaxValue) >= 1;

            if (hasPork && hasOil && hasSugar)
            {
                Game1.player.Items.ReduceId("(O)184", 1);
                Game1.player.Items.ReduceId("(O)247", 1);
                Game1.player.Items.ReduceId("(O)245", 1);
                CompleteQuest(QuestDongpo, modData);
                Game1.player.Money += 2000;
                npcManager.SetDialogue("SuShi",
                    "妙哉！这食材正合我意。$h#$b#" +
                    "\"净洗铛，少著水，柴头罨烟焰不起。\"$s#$b#" +
                    "这便是东坡肉的秘诀——慢火细炖，方得醇香。");
                modData.NpcStates["SuShi"].DialogueStage = 3;
            }
        }

        private void CheckAllQuestsComplete(ModData modData)
        {
            if (modData.AllQuestsComplete)
                return;

            if (modData.CompletedQuests.Contains(QuestCauseway) &&
                modData.CompletedQuests.Contains(QuestDongpo) &&
                modData.CompletedQuests.Contains(QuestPoetry) &&
                modData.CompletedQuests.Contains(QuestZen))
            {
                modData.AllQuestsComplete = true;
                Game1.addHUDMessage(new HUDMessage("三位北宋灵魂的祝福汇聚在一起，化为星露谷的守护之力。", 2));
            }
        }
    }
}
