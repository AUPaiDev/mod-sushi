using System.Collections.Generic;

namespace SuShiLegend
{
    public class ModData
    {
        public bool StoneTabletFound { get; set; }
        public Dictionary<string, NpcState> NpcStates { get; set; } = new()
        {
            ["SuShi"] = new NpcState(),
            ["Zhaoyun"] = new NpcState(),
            ["Foyin"] = new NpcState()
        };
        public HashSet<string> CompletedQuests { get; set; } = new();
        public HashSet<string> ActiveQuests { get; set; } = new();
        public int FoyinRiddleProgress { get; set; }
        public int PoetryPagesFound { get; set; }
        public bool AllQuestsComplete { get; set; }
    }

    public class NpcState
    {
        public int DialogueStage { get; set; }
        public int FriendshipPoints { get; set; }
    }
}
