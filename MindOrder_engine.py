# -*- coding: utf-8 -*-
"""
================================================================================
心秩学判定引擎 · 公理结构 v3.0 / 数据与判定 v3.8
================================================================================
版本说明：
  · 公理结构自 v3.0 起未再变动（四次公理 + 一条元规则）
  · v3.1—v3.8 均为该结构下的补丁：证据补全、编号收敛、参数稳健性
  · 故此处分开标注：引擎结构 v3.0，案例数据与判定规则 v3.8

v2.x 是涌现式增长（每次讨论补几条规则），v3.0 做减法：
    把所有修订收敛为 **4 条公理 + 1 条元规则 + 若干推论**。

【四条公理】（不可再分，一切规则的源头）
  A1 客观唯物主义   物质决定意识；真理与大势客观，个人认知有限
  A2 绝对人道底线   非战斗人员生命/基础财产不可侵犯；公理，非概率
  A3 分维度独立定级 不综合打分；单一维度至圣即至圣
  A4 此时此地       以当前时点、此地视角评判

【一条元规则】
  M0 明得失、知进退 目标不是考古复原，是复盘

【推论】（全部由公理推出，不新增独立规则）
  C1 无罪推定      ← A1（客观，不预设恶意）
  C2 只处理已知    ← A1（预言不进入计量）
  C3 min 原则      ← A3（慈秩博取短板，恶行/盲区不被掩盖）
  C4 褒奖权归各维度 ← A3（动机问题由慈承担，不在他维重复惩罚）
  C5 禁止双重惩罚  ← A3（同一事实不判两次）
  C6 主体分离      ← A3（政权/遗产、个人/制度各判）
  C7 准入与地板    ← M0+A3（入口筛：无创造与贡献者不入体系；
                            出口筛：有维度达精英者不判地板。同一原则两面）
  C8 降工规则      ← A3+工定义（缺失负反馈设计 → 工降一档）
  C9 视角相对·底线绝对 ← A4+A2（输入可变，底线不可变）
  C10 分段内独立身份适配 ← A3（身份在分段间变化时，各段按该段身份定标）
  C11 贡献以受益对象计 ← A1（贡献以"收益留在谁手里"计量，非活动规模）
================================================================================
"""
import json, math

# ───────────────────── 维度定义（A3 的载体）─────────────────────
L = {"无": 0, "普世以下": 1, "普世": 2, "精英": 3, "至圣": 4}
L_INV = {v: k for k, v in L.items()}

# 四维分工（四维各褒奖各自的事，不做道德叠加评价）
DIM_ROLE = {
    "慈": "动机",   # 出发点是否指向群体福祉
    "秩": "有效性", # 秩序是否真在运转（不承担道德判断）
    "博": "认知",   # 对边界与规律的洞察
    "工": "行动",   # 造没造出来、活没活下来（不管道不道德）
}

# 三层段位（四字诀）
VERB = {
    "慈": {"普世": "慈以待人", "精英": "慈以护民", "至圣": "慈以润世",
           "无": "慈已背离", "普世以下": "慈有亏缺"},
    "秩": {"普世": "秩以循规", "精英": "秩以立规", "至圣": "秩以定纲",
           "无": "秩已破缺", "普世以下": "秩有松动"},
    "博": {"普世": "博以明辨", "精英": "博以求知", "至圣": "博以探源",
           "无": "博已蔽塞", "普世以下": "博有盲区"},
    "工": {"普世": "工以笃行", "精英": "工以精业", "至圣": "工以造物",
           "无": "工已荒废", "普世以下": "工未落地"},
}

# 主体类型的四维映射（C6 主体分离的具体化）
SUBJECT_MAP = {
    "人物": "慈=利他行为 秩=秩序建设 博=认知探源 工=落地成果",
    "制度": "慈=普惠程度 秩=秩序框架 博=设计深度 工=存续时效",
    "思潮": "慈=理念利他(看初心) 秩=是否成秩序框架 博=探源深度 工=被践行程度",
    "法律": "慈=min(对内公正,对外底线) 秩=覆盖力·可预期性·多数认同·司法独立 博=法理穿透力 工=存续×执行率×纠错",
    "法系": "慈=min(对内公正,对外底线遵守)　秩=秩序生成方式与效力（成文法/判例法/神启法各有其生成机制）　博=是否理解立法与司法的深层规律　工=典范影响范围×存续年限×自我演进能力",
    "国家": "慈=min(民生,对内公正,对外底线) 秩=min(局部,全局,对外主权) 博=min(地缘,生产力) 工=治理年限×效能×自我修复",
    "组织": "慈=min(内部公平,外部普惠) 秩=商业/行业秩序重构 博=行业与生产力边界认知 工=产品与商业成果",
}

TAG_PRIORITY = ["地板", "底线破缺型", "破局型", "崩坏型", "未兑现型", "模板型",
                "残缺型", "均衡偏科型", "救济型", "失职型", "达标型·有瑕", "达标型"]

# 经验阈值（非精确推导）。取值依据：在经验稳定带内，取与「痛苦不对称性」
# 最一致（即最严厉）的端点。敏感性分析实测（v3.8，172 例）：
#   DESTROY_WEIGHT 层级稳定带 [1.0,1.6]，当前 1.5；≥1.7 董卓翻案，≥2.0 纳粹翻案，≥2.5 滇越翻案
#   SEVERE_RATIO   层级稳定带 [1.4,2.2]，当前 1.5（下沿）
#   MAX_REDUCTION  =2 为唯一零变动值
#   CONF_THRESHOLD=0.6；撤置信度折减（阈值→0）：层级 3 / 标签 3（隋炀帝、王莽、周幽王，均带待考）
DESTROY_WEIGHT = 1.5      # 痛苦不对称性：破坏项加权后比对
MAX_REDUCTION = 2         # 数罪并罚，总降档上限
CONF_THRESHOLD = 0.6      # 先验置信度阈值（C1 疑罪从有利）
SEVERE_RATIO = 1.5

NATION = {"国家", "王朝", "帝国", "政权"}


def norm(v):
    return round(min(10.0, math.log10(max(v, 0) + 1) / 1.4), 2)


def raw_benefit(b):
    return max(b.get("people", 0), 0) * max(b.get("years", 0), 0)


def raw_harm(h, attribution=1.0):
    if not h:
        return 0.0
    base = (max(h.get("people", 0), 0) * max(h.get("years", 0), 0)
            * max(h.get("intensity", 1.0), 0.1))
    return base * attribution


def cap(x):
    return max(0, x - 1)


# ═══════════════ 阶段一：先验（A4 此时此地 / C9 视角相对）═══════════════
def stage1_prior(lens):
    return {
        "视角": lens.get("name", "默认"), "来源": lens.get("source", "主流历史共识"),
        "偏见方向": lens.get("bias", "未标注"), "置信度": lens.get("confidence", 0.8),
        "归因系数": lens.get("attribution", 1.0),
        "提示": "先验有偏是特性（C9）——目标为明得失，非考古复原",
    }


# ═══════════════ 阶段二：五步法 ═══════════════
def stage2_five_steps(case, lens, flags, defects):
    evid, segs = case["evid"], case["segments"]

    # ── C3 min 原则：慈取各段最小值，秩博工取最大值 ──
    ci_seg = min(L[s[1]] for s in segs)
    zhi_seg = max(L[s[2]] for s in segs)
    bo_seg = max(L[s[3]] for s in segs)
    gong_seg = max(L[s[4]] for s in segs)
    if len(segs) > 1:
        flags.append("分段评价：慈取 min（恶行不被善行掩盖），秩博工取 max（成就不被崩塌抹杀）")

    # ── 第一步 C1 无罪推定：默认普世层基础信任 ──
    flags.append("第一步 无罪推定：默认普世层基础信任，须有实证方可降级")

    # ── 第二步 事实证伪：秩破局三分 ──
    zhi = zhi_seg
    if zhi == 0:
        bt = evid.get("秩_破局类型", "失职")
        if bt == "恶性":
            flags.append("第二步 秩归零·恶性破局：秩序正常而蓄意破坏 → 记降档因子")
        elif bt == "救济":
            if evid.get("救济_收敛回平衡"):
                flags.append("第二步 秩归零·救济型破局 → 免责不加分（收敛检验通过）")
            else:
                flags.append("第二步 救济型破局**收敛失败** → 改判恶性破局")
                flags.append("REMEDY_FAILED")
        elif bt == "价值挑战":
            if evid.get("思想_主张违反底线"):
                flags.append("第二步 价值挑战**豁免失效**：主张违反 A2 → 触发底线")
                flags.append("THINKER_BREACH")
            else:
                flags.append("第二步 价值挑战：思维实验 → 鼓励，不降档")

    # ── 第二步 博至圣三条件（C7 准入：无体系性认知者不入至圣）──
    bo = bo_seg
    if bo == 4:
        if not evid.get("博_自圆其说"):
            bo = 3; defects.append("博未自圆其说 → 降为精英")
        if evid.get("博_违背可验证事实"):
            bo = 3; defects.append("博违背可验证事实 → 降为精英")
        if not evid.get("博_体系性认知"):
            bo = 3; defects.append("博未形成体系性认知 → 降为精英")
    # C3 博取短板：盲区不被洞见掩盖
    if case.get("identity") in NATION and evid.get("博_地缘") and evid.get("博_生产力"):
        flags.append("博取 min(地缘, 生产力)：盲区不被洞见掩盖")

    # ── 第二步 工至圣三条件（C8：无负反馈设计者降工）──
    gong = gong_seg
    if gong == 4:
        miss = [k for k in ("工_突破范式", "工_改变运行逻辑", "工_长期存续有效")
                if not evid.get(k)]
        if miss:
            gong = 3; defects.append("工缺条件「%s」→ 降为精英" % "、".join(miss))
    # C8 降工规则：缺失负反馈设计 → 工降一档
    # （v3.8 名实对齐：原实现只记缺陷、不改判定，名为「降工」却从不降档）
    if gong >= 3 and evid.get("工_自我修复") is False:
        gong = gong - 1
        defects.append("C8 降工规则：缺失负反馈设计 → 工由「%s」降为「%s」（防扭曲锁缺失，造物不算完整）"
                       % (L_INV[gong + 1], L_INV[gong]))

    # ── 第二步 A2 绝对人道底线 ──
    bottom_hit = bool(evid.get("底线_治理性剥夺")) or ("THINKER_BREACH" in flags)
    benevolent = evid.get("慈_主动护民行为")
    betrayal = evid.get("慈_主动背离善意", False)
    if bottom_hit:
        ci = 0
        flags.append("A2 绝对人道底线击穿：治理性/制度性剥夺 → 慈归零 + 记降档因子")
    elif betrayal and not benevolent:
        ci = 0
        flags.append("慈归零：主动背离善意，且无可验证的护民行为")
    elif betrayal and benevolent:
        ci = max(ci_seg, {"个人": 2, "群体": 3, "文明": 4}.get(benevolent, 2))
        defects.append("存在主动背离善意的暴行，但护民行为成立 → 记重大缺陷，慈不归零")
    else:
        ci = ci_seg
    if evid.get("慈_非必要暴行"):
        defects.append("非必要牺牲/暴行（初心或相称性不符）→ 慈维度缺陷记录")

    # ── 第三步 身份适配 + 时间动态 ──
    ident = case.get("identity")
    if ident == "执政者" and zhi >= 4:
        flags.append("第三步 身份适配：执政型至圣，套用秩慈兑换律（看初心与相称性）")
    # 局部秩 vs 全局秩
    zl, zg = evid.get("秩_局部"), evid.get("秩_全局")
    if zl and zg:
        lo, hi = L[zl], L[zg]
        zhi = min(lo, hi)
        if abs(lo - hi) >= 2:
            flags.append("**局部秩=%s / 全局秩=%s → 取 min=%s，差 %d 档**" % (
                zl, zg, L_INV[zhi], abs(lo - hi)))
            flags.append("    **秩失衡·不稳定前兆**：局部强而全局弱，是秩滑向崩塌的诊断信号")
        else:
            flags.append("局部秩=%s / 全局秩=%s → 取 min=%s（未失衡）" % (zl, zg, L_INV[zhi]))

    return ci, zhi, bo, gong, bottom_hit


# ═══════════════ 阶段三：决策树（第四步 + 第五步）══════════════
def stage3_decision_tree(case, lens, ci, zhi, bo, gong, bottom_hit, flags, defects):
    dims = {"慈": ci, "秩": zhi, "博": bo, "工": gong}
    top = max(dims.values())
    evid = case["evid"]
    conf = lens.get("confidence", 0.8)

    # ── 第四步 休谟抉择（C2 只处理已知；C5 不重复计入底线危害）──
    contrib_raw = raw_benefit(lens.get("benefit_override") or case.get("benefit") or {})
    destroy_bottom = raw_harm(case.get("bottom_harm"), attribution=1.0)
    destroy_general = raw_harm(case.get("general_harm"),
                               attribution=lens.get("attribution", 1.0))
    destroy_raw = destroy_general if bottom_hit else (destroy_bottom + destroy_general)

    ratio = (destroy_raw * DESTROY_WEIGHT / contrib_raw) if contrib_raw > 0 else (
        float("inf") if (destroy_raw > 0 and top >= 3) else 0.0)
    # C1 疑罪从有利：证据越不可靠，越难定罪
    ratio_adj = ratio * math.sqrt(conf) if conf < CONF_THRESHOLD else ratio
    severe = ratio_adj >= SEVERE_RATIO
    negative = ratio_adj >= 1.0

    if severe:
        step4 = "剔除正向价值（加权比值 %.3f ≥ %.1f）" % (ratio_adj, SEVERE_RATIO)
    elif negative:
        step4 = "损益接近，降一档 + 强负反馈围栏（比值 %.3f）" % ratio_adj
    else:
        step4 = "保留价值，架设负反馈围栏（比值 %.3f）" % ratio_adj
    if conf < CONF_THRESHOLD:
        step4 += "｜置信度 %.2f < %.1f → 疑罪从有利，比值按 √置信度 折减（%.3f→%.3f）" % (
            conf, CONF_THRESHOLD, ratio, ratio_adj)
    flags.append("第四步 休谟抉择：%s%s" % (
        step4, "　｜　底线危害不重复计入（C5）" if bottom_hit else ""))

    # ── 降档因子：数罪并罚，总上限 2 档 ──
    seg_count = len(case.get("segments") or [])
    factors = []
    if bottom_hit:
        factors.append("底线击穿")
    if zhi == 0 and (evid.get("秩_破局类型") == "恶性" or "REMEDY_FAILED" in flags):
        factors.append("恶性破局")
    elif seg_count > 1 and evid.get("秩_破局类型") == "恶性" and zhi > 0:
        flags.append("分段时恶性破局已由「秩取 max」吸收 → 不重复降档（C5），保留破局型标签")
    if gong < 3 and top == 4:
        factors.append("工未兑现")
    if negative and top >= 3 and not severe:
        factors.append("损益对冲")
    reduction = min(len(factors), MAX_REDUCTION)
    lev = max(0, top - reduction)
    if severe and negative:
        lev = min(lev, 1)
    flags.append(("降档因子（数罪并罚，上限 %d）：%s → 降 %d 档" % (
        MAX_REDUCTION, " + ".join(factors), reduction)) if factors else "降档因子：无")

    # ── 标签 ──
    tags = set()
    if zhi == 0 and (evid.get("秩_破局类型") == "恶性" or "REMEDY_FAILED" in flags):
        tags.add("破局型")
    elif any(len(s) >= 3 and s[2] == "无" and evid.get("秩_破局类型") == "恶性"
             for s in (case.get("segments") or [])):
        tags.add("破局型")
    if bottom_hit:
        tags.add("底线破缺型")
    if gong < 3 and top == 4:
        tags.add("崩坏型") if (negative and severe) else tags.add("未兑现型")
    if top == 4 and all(v == 4 for v in dims.values()):
        tags.add("模板型")
    # 档位出口（v3.8）：让每一档都在标签中可见。此前只有 0 档可见，
    # 1 档（普世以下）与 2 档（普世）完全不参与判定 —— 即「维度悬空」。
    DIM_ORDER = ("慈", "秩", "博", "工")
    zero_dims     = [k for k in DIM_ORDER if dims[k] == 0]  # 无
    collapse_dims = [k for k in DIM_ORDER if dims[k] == 1]  # 普世以下 → 塌陷
    thin_dims     = [k for k in DIM_ORDER if dims[k] == 2]  # 普世     → 薄弱
    if top == 4:
        if zero_dims or evid.get("慈_非必要暴行") or (gong == 3):
            tags.add("残缺型")
        else:
            tags.add("均衡偏科型")
    if zhi == 0 and evid.get("秩_破局类型") == "救济" and evid.get("救济_收敛回平衡"):
        tags.add("救济型")
    elif zhi == 0 and evid.get("秩_破局类型", "") not in ("恶性", "救济"):
        tags.add("失职型")

    # C7 准入与地板：定性 0 档 且 无任何维度达精英
    has_elite = any(v >= L["精英"] for v in dims.values())
    if lev == 0 and not has_elite and (zhi == 0 and evid.get("秩_破局类型") == "恶性"):
        tags.add("地板")
    elif lev == 0 and has_elite:
        flags.append("C9 未判地板：存在精英以上维度（%s）——能被分析者，皆有可吸取之处"
                     % "、".join(k for k, v in dims.items() if v >= L["精英"]))

    flawed = bool(defects) or ci == 0 or zhi == 0 or bool(evid.get("慈_非必要暴行"))
    label = next((t for t in TAG_PRIORITY if t in tags), "达标型")
    if label == "达标型" and flawed and top <= 3:
        label = "达标型·有瑕"

    suffix = []
    if zero_dims:
        suffix.append("、".join(zero_dims) + "为无")
    if collapse_dims:
        suffix.append("、".join(collapse_dims) + "塌陷")
    if thin_dims:
        suffix.append("、".join(thin_dims) + "薄弱")
    if gong == 3 and top == 4:
        suffix.append("部分兑现")
    if len(case["segments"]) > 1:
        st = case["segments"]
        f_top = max(L[st[0][2]], L[st[0][3]], L[st[0][4]])
        l_top = max(L[st[-1][2]], L[st[-1][3]], L[st[-1][4]])
        if l_top < f_top:
            suffix.append("分段崩塌")
        elif L[st[-1][1]] < L[st[0][1]]:
            suffix.append("慈分段下滑")
    if conf < CONF_THRESHOLD:
        suffix.append("待考")
    full = label + ("·" + "·".join(suffix) if suffix else "")

    # ── 第五步 负反馈 ──
    flags.append("第五步 分级负反馈：常规→律法合同/舆论监督/分权制衡/谏官体系；"
                 "极端救世→仅当慈秩双归零+制度全面失灵时启用")

    # ── 四维各自标签（复盘导向）──
    dim_labels = {d: _dim_label(d, dims[d], case, flags, bottom_hit) for d in ("慈", "秩", "博", "工")}

    return (L_INV[lev] if lev > 0 else "反面教材"), full, dim_labels, {
        "contrib": norm(contrib_raw), "destroy": norm(destroy_raw),
        "ratio": ratio, "ratio_adj": ratio_adj, "factors": factors,
    }


def _dim_label(d, level, case, flags, bottom_hit):
    name = L_INV[level]
    parts = ["%s（%s=%s，%s）" % (name, d, DIM_ROLE[d], VERB[d][name])]
    evid = case["evid"]
    if d == "慈":
        if bottom_hit:
            parts.append("底线击穿")
        if evid.get("慈_短板"):
            parts.append("短板=%s" % evid["慈_短板"])
        if evid.get("慈_内部") or evid.get("慈_外部"):
            parts.append("min(内部=%s, 外部=%s)" % (
                evid.get("慈_内部", "?"), evid.get("慈_外部", "?")))
        if evid.get("慈_非必要暴行"):
            parts.append("非必要暴行")
    elif d == "秩":
        if evid.get("秩_短板"):
            parts.append("短板=%s" % evid["秩_短板"])
        if level == 0:
            parts.append({"恶性": "恶性破局", "救济": "救济型破局",
                          "价值挑战": "价值挑战", "失职": "失职"}.get(
                              evid.get("秩_破局类型", "失职"), "失职"))
        if evid.get("秩_崩塌信号"):
            parts.append("崩塌信号=%s" % evid["秩_崩塌信号"])
    elif d == "博":
        geo, prod = evid.get("博_地缘"), evid.get("博_生产力")
        if geo and prod:
            parts.append("地缘=%s" % geo)
            parts.append("生产力=%s" % prod)
        if evid.get("博_行业"):
            parts.append("行业=%s" % evid["博_行业"])
        if evid.get("博_违背可验证事实"):
            parts.append("违背事实")
    elif d == "工":
        if evid.get("工_自我修复") is False:
            parts.append("无自我修复")
        if evid.get("工_效能"):
            parts.append("效能=%s" % evid["工_效能"])
        if level < 3:
            parts.append("未兑现")
        elif level == 3:
            parts.append("部分兑现")
    return " · ".join(p for p in parts if p)


def evaluate(case, lens):
    flags, defects = [], []
    prior = stage1_prior(lens)
    ci, zhi, bo, gong, bottom_hit = stage2_five_steps(case, lens, flags, defects)
    lev_name, label, dim_labels, m = stage3_decision_tree(
        case, lens, ci, zhi, bo, gong, bottom_hit, flags, defects)
    return {
        "name": case["name"], "lens": lens.get("name"), "identity": case.get("identity"),
        "慈": L_INV[ci], "秩": L_INV[zhi], "博": L_INV[bo], "工": L_INV[gong],
        "定性": "%s（%s）" % (lev_name, label), "标签": label,
        "四维标签": dim_labels, "flags": flags, "defects": defects,
        "prior": prior, "metric": m, "expected": case.get("expected", ""),
        "bottom_hit": bottom_hit,
    }


def evaluate_all(case):
    results = [evaluate(case, ln) for ln in case["lenses"]]
    invariant = len({r["bottom_hit"] for r in results}) == 1
    lv = [L.get(r["定性"].split("（")[0], 0) for r in results]
    return results, invariant, (max(lv) - min(lv))


def load(path="data/cases.json"):
    return json.load(open(path, encoding="utf-8"))


def primary(runs):
    return runs[0]


def main():
    data = load()
    cases, demos = data["cases"], data["demos"]
    print("=" * 106)
    print("心秩学判定引擎 v3.8 · 全量复算（4 公理 + 1 元规则 + 11 条推论）")
    print("=" * 106)
    ok = 0
    for c in cases:
        r = primary(evaluate_all(c)[0])
        match = (r["定性"] == r["expected"])
        ok += 1 if match else 0
        print("\n【%s】%s　%s" % (r["name"], "✓" if match else "✗", r["identity"]))
        for d in ("慈", "秩", "博", "工"):
            print("  %s：%s" % (d, r["四维标签"][d]))
        print("  ▶ %s" % r["定性"])
        if not match:
            print("     预期：%s" % r["expected"])
    print("\n主案例一致 %d / %d" % (ok, len(cases)))

    dok = 0
    print("\n" + "=" * 106)
    print("演示 / 边缘测试 / 盲测")
    print("=" * 106)
    for c in demos:
        r = primary(evaluate_all(c)[0])
        match = (r["定性"] == r["expected"])
        dok += 1 if match else 0
        print("\n【%s】%s" % (r["name"], "✓" if match else "✗"))
        for d in ("慈", "秩", "博", "工"):
            print("  %s：%s" % (d, r["四维标签"][d]))
        print("  ▶ %s" % r["定性"])
        if not match:
            print("     预期：%s" % r["expected"])
    print("\n演示一致 %d / %d" % (dok, len(demos)))

    print("\n" + "=" * 106)
    print("多视角并列（C9：视角相对，底线绝对）")
    print("=" * 106)
    for c in cases + demos:
        if len(c["lenses"]) < 2:
            continue
        runs, inv, spread = evaluate_all(c)
        print("\n【%s】" % c["name"])
        for r in runs:
            print("  · %-18s → %s" % (r["lens"], r["定性"]))
        print("  不变量检验：底线跨视角一致 = %s　层级跨度 = %d 档%s" % (
            "✓" if inv else "✗ 违反", spread, "　→ 强视角依赖" if spread >= 2 else ""))

    print("\n" + "=" * 106)
    print("v3.0 减法：v2.x 的 50+ 条修订 → 4 公理 + 1 元规则 + 11 条推论（v3.7 合并 C7/C9 后收敛）")
    print("=" * 106)
    for k, v in SUBJECT_MAP.items():
        print("  %-6s %s" % (k, v))


if __name__ == "__main__":
    main()
