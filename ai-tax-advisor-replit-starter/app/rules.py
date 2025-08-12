
from typing import Dict, List, Set

def run_rules(forms: Set[str], fields: Dict, raw_text: str) -> List[Dict]:
    """
    Example 'opportunity' rules. Replace with your real rule engine later.
    """
    recs = []

    def add(card):
        # Enforce a minimal shape so the UI can render consistently
        base = {
            "title": "",
            "category": "",
            "estimate_savings_range": [0, 0],
            "confidence": 0.5,
            "reason": "",
            "actions": []
        }
        base.update(card)
        recs.append(base)

    # QBI missing
    if ("schedule c" in forms or "k-1" in forms or "schedule e" in forms) and ("8995" not in forms):
        add({
            "title": "QBI(§199A) 공제 검토 필요",
            "category": "QBI",
            "estimate_savings_range": [300, 3500],
            "confidence": 0.6,
            "reason": "사업/패스스루 소득이 보이나 Form 8995 흔적이 없습니다.",
            "actions": ["사업 유형(SSTB) 확인", "과세소득 한계/임계값 점검", "8995 계산 워크시트 작성"]
        })

    # HSA potential
    if fields.get("hsa_hint") and "form 8889" not in forms:
        add({
            "title": "HSA 보고/공제 확인",
            "category": "HSA",
            "estimate_savings_range": [100, 1200],
            "confidence": 0.55,
            "reason": "HSA 관련 키워드는 보이나 8889 양식이 보이지 않습니다.",
            "actions": ["HDHP 가입 여부 확인", "HSA 납입/분배 내역 수집", "8889 작성 여부 확인"]
        })

    # Itemized vs Standard
    if fields.get("mortgage_interest_hint") and "schedule a" not in forms:
        add({
            "title": "항목별 공제(Schedule A) 전환 검토",
            "category": "Itemized",
            "estimate_savings_range": [0, 2000],
            "confidence": 0.5,
            "reason": "모기지 이자/1098 흔적은 보이나 Schedule A가 감지되지 않습니다.",
            "actions": ["SALT 상한/표준공제 비교", "모기지 이자/재산세 증빙 확인"]
        })

    # Child/Dependent Care Credit
    if fields.get("dependents_section_present") and "2441" not in forms:
        add({
            "title": "Dependent Care Credit 가능성",
            "category": "Credit",
            "estimate_savings_range": [0, 600],
            "confidence": 0.45,
            "reason": "Dependent 섹션이 보이나 Form 2441이 감지되지 않습니다.",
            "actions": ["피보험자 나이 확인(<13)", "보육비 영수증 수집"]
        })

    # Education credit
    if fields.get("education_hint") and "8863" not in forms:
        add({
            "title": "교육 크레딧(AOTC/LLC) 검토",
            "category": "Education",
            "estimate_savings_range": [0, 2500],
            "confidence": 0.5,
            "reason": "교육 관련 키워드가 보이나 8863 양식이 감지되지 않습니다.",
            "actions": ["1098-T 확인", "장학금/현금지출 반영", "AOTC/LLC 자격 판별"]
        })

    return recs
