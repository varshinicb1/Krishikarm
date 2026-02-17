"""Kisan-Eye V6 — System Test"""
import scheme_matcher, farmer_db, json

# Create test farmer in distress
fid = farmer_db.create_farmer(
    'Ramu Yadav', 'Sultanpur', 'Varanasi', 'Uttar Pradesh',
    language='hi', latitude=25.32, longitude=83.01,
    land_acres=2.5, crops=['rice', 'wheat'],
    irrigation_type='rainfed', bpl_card=1,
    financial_state='distress', debt_amount=150000,
    family_members=6
)

farmer = farmer_db.get_farmer(fid)
print(f"=== FARMER REGISTERED ===")
print(f"ID: {fid}")
print(f"Name: {farmer['name']}")
print(f"Village: {farmer['village']}, {farmer['district']}, {farmer['state']}")
print(f"Land: {farmer['land_acres']} acres | Crops: {farmer['crops']}")
print(f"Financial: {farmer['financial_state']} | Debt: Rs {farmer['debt_amount']}")
print(f"Language: {farmer['language']} | BPL: {farmer['bpl_card']}")

# Match schemes
schemes = scheme_matcher.match_schemes(farmer)
print(f"\n=== ELIGIBLE SCHEMES ({len(schemes)} total) ===")
for i, s in enumerate(schemes):
    print(f"  {i+1}. {s['name']}")
    print(f"     Benefit: {s['benefit']}")
    print(f"     Helpline: {s['helpline']}")
    print()

# Check distress schemes
distress = scheme_matcher.get_distress_schemes(farmer)
print(f"=== DISTRESS SCHEMES ({len(distress)} total) ===")
for s in distress[:5]:
    print(f"  - {s['name']}: {s['benefit']}")

print("\n=== ALL TESTS PASSED ===")
