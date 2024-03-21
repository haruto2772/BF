import streamlit as st
import BF_stMain as stM
import BF_ObjectDef as OB

def ca():
    st.session_state["page_control"] = 3

def ea():
    st.session_state["page_control"] = 4

def change_BFinit(BF):
    st.session_state["BF"] = BF
    st.session_state["ShopList"] = []
    st.session_state["page_control"] = 5

def Town_command():
    st.sidebar.button("Town Shop", on_click = stM.change_Shop)
    st.sidebar.button("Town Enchant", on_click = stM.change_Enchant)
    st.sidebar.button("Town AddSlot", on_click = ca)
    st.sidebar.button("Town Elder Advice", on_click = ea)
    BF1 = "BF " + st.session_state["BF1"].StageName
    BF2 = "BF " + st.session_state["BF2"].StageName
    if BF1 != "BF none":
        st.sidebar.button(BF1, on_click = change_BFinit, args = [st.session_state["BF1"]])
    if BF2 != "BF none":
        st.sidebar.button(BF2, on_click = change_BFinit, args = [st.session_state["BF2"]])

def buy_ShopItem(cnt, x):
    if st.session_state["Player"].gold < 20:
        st.write("You have not enogh money!")
        st.button("Return", on_click = stM.change_Town())  
        return
    del st.session_state["ShopList"][cnt-1]
    st.session_state["Player"].gold -= 20
    if x.species == "Weapon":
        st.session_state["NewWeapon"] = x
        st.session_state["page_control"] = 11
        #stBF.SelectWeapon()
    elif x.species == "Armor":
        st.session_state["NewArmor"] = x
        st.session_state["page_control"] = 12
        #stBF.SelectArmor()    
    elif x.species == "Scroll":
        st.session_state["NewScroll"] = x
        st.session_state["page_control"] = 13
        #stBF.SelectScroll()
    elif x.species == "Crystal":
        st.session_state["NewCrystal"] = x
        st.session_state["page_control"] = 14
        #stBF.SelectCrystal(False)
    else:
        st.write("Irregal Item")
    
    #del st.session_state["ShopList"][cnt-1]
    #st.session_state["page_control"] = 1

def Town():
    st.session_state["Player"].CalcBattleStatus
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.subheader("Town")
    Town_command()

def Shop():
    st.session_state["Player"].CalcBattleStatus
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.subheader("Equipment Shop")
    st.write("All item's price are 20 gold.")
    if st.session_state["ShopList"] == []:
        st.write("There is no line-up.")
        st.button("Return", on_click = stM.change_Town())
        return
    cnt = 0
    for x in st.session_state["ShopList"]:
        cnt += 1
        if x.species == "Weapon":
            text = x.name + ":" + str(x.Atk1) + "d" + str(x.Atk2)
        elif x.species == "Armor":
            text = x.name + ":" + str(x.def1) + ", " + str(x.MGR)
        elif x.species == "Scroll":
            text = x.name
        elif x.species == "Crystal":
            text = x.name
        else:
            text = "none"
        st.button(text, key = cnt, on_click = buy_ShopItem, args = [cnt, x])  
    #st.sidebar.button("Town", on_click = stM.change_Town)
    st.button("Return", on_click = stM.change_Town)
        
def Enchant_Weapon():
    if st.session_state.WEcost[0] == 9999:
        st.write("Your Weapon is Max Enchanted!")
    elif st.session_state["Player"].gold > st.session_state.WEcost[0]:
        EVal = st.session_state.WEcost[1]
        st.write(f"Weapon is enchanted! +{EVal}")
        st.session_state["Player"].gold -= st.session_state.WEcost[0]
        st.session_state["Player"].Weapon.AddEnchant(EVal)
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory)
    else:
        st.write("You have not enogh money!")
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.button("Return", on_click = stM.change_Enchant)

def Enchant_Armor():
    cost = st.session_state.AEcost[0]
    if cost == 9999:
        st.write("Your Armor is Max Enchanted!")
    elif st.session_state["Player"].gold > cost:
        EVal = st.session_state.AEcost[1]
        MGRVal = st.session_state.AEcost[2]
        st.write(f"Armor is enchanted! Def +{EVal}")
        st.write(f"Armor is enchanted! MGR +{MGRVal}")
        st.session_state["Player"].gold -= cost
        st.session_state["Player"].Armor.AddEnchant(EVal, MGRVal)
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory)
    else:
        st.write("You have not enogh money!")
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.button("Return", on_click = stM.change_Enchant)

def change_Enchant_Weapon():
    st.session_state["page_control"] = 21

def change_Enchant_Armor():
    st.session_state["page_control"] = 22

def Enchant():
    st.session_state["Player"].CalcBattleStatus
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.subheader("Enchant Workshop")    
    st.write("Select Enchant for ")
    WVal = st.session_state["Player"].Weapon.enum
    if WVal > 4:
        #st.write("Max Enchanted!")
        Wcost = 9999
        WEVal = 0
    elif WVal == 4:
        Wcost = 500
        WEVal = OB.DiceRoll(4,6)
    elif WVal == 3:
        Wcost = 200
        WEVal = OB.DiceRoll(3,6)
    elif WVal == 2:
        Wcost = 100
        WEVal = OB.DiceRoll(2,6)
    elif WVal == 1:
        Wcost = 50
        WEVal = OB.DiceRoll(2,4)
    else:
        Wcost = 20
        WEVal = OB.DiceRoll(1,4)
    AVal = st.session_state["Player"].Armor.enum
    if AVal > 4:
        #st.write("Max Enchanted!")
        Acost = 9999
        AEVal = 0
        MGRVal = 0
    elif AVal == 4:
        Acost = 500
        AEVal = OB.DiceRoll(4,6)
        MGRVal = OB.DiceRoll(1, 4)
    elif AVal == 3:
        Acost = 200
        AEVal = OB.DiceRoll(3,6)
        MGRVal = OB.DiceRoll(1, 4)
    elif AVal == 2:
        Acost = 100
        AEVal = OB.DiceRoll(2,6)
        MGRVal = OB.DiceRoll(1, 4)
    elif AVal == 1:
        Acost = 50
        AEVal = OB.DiceRoll(2,4)
        MGRVal = OB.DiceRoll(1, 4)
    else:
        Acost = 20
        AEVal = OB.DiceRoll(1,4)
        MGRVal = OB.DiceRoll(1, 4)
    st.session_state.WEcost = [Wcost, WEVal]
    if Wcost == 9999:
        st.write("Your Weapon is Max Enchanted!")
    else:
        st.write(f"Weapon cost is {Wcost} gold.")
        st.button("Weapon", on_click = change_Enchant_Weapon)
    st.session_state.AEcost = [Acost, AEVal, MGRVal]
    if Acost == 9999:
        st.write("Your Armor is Max Enchanted!")
    else:    
        st.write(f"Armor cost is {Acost} gold.")
        st.button("Armor", on_click = change_Enchant_Armor)
    st.button("Return", on_click = stM.change_Town)

def AddSlot_Weapon():
    #st.write(st.session_state["Player"].Weapon.slot)
    if st.session_state["Player"].Weapon.slot > 0:
        st.write("Your Weapon Slot is Max!")
    elif st.session_state["Player"].gold > 200:
        st.write("Add Slot Weapon +1!")
        st.session_state["Player"].gold -= 200
        st.session_state["Player"].Weapon.AddSlot()
    else:
        st.write("You have not enogh gold!")
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.button("Return", on_click = ca)

def AddSlot_Armor():
    if st.session_state["Player"].Armor.slot > 0:
        st.write("Your Armor Slot is Max!")
    elif st.session_state["Player"].gold > 200:
        st.write("Add Slot Armor +1!")
        st.session_state["Player"].gold -= 200
        st.session_state["Player"].Armor.AddSlot()
    else:
        st.write("You have not enogh gold!")
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.button("Return", on_click = ca)

def change_AddSlot_Weapon():
    st.session_state["page_control"] = 31

def change_AddSlot_Armor():
    st.session_state["page_control"] = 32

def AddSlot():
    st.session_state["Player"].CalcBattleStatus
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.subheader("AddSlot Workshop") 
    st.write("Max Equip Slot is 1.")
    st.write("Add Slot cost is 200 gold.")    
    st.write("Select Enchant for ") 
    st.button("Weapon", on_click = change_AddSlot_Weapon)
    st.button("Armor", on_click = change_AddSlot_Armor)
    st.button("Return", on_click = stM.change_Town)

def ElderAdvice():
    st.sidebar.header("BF 1.2")
    stM.DispPStatus()
    st.subheader("Elder's Advice") 
    if st.session_state["Player"].Lv == 1:
        st.write("Welcome to probability forest!  \n \
                  First, you must be get 2d8 - 3d10 Dagger or ShortSword.  \n \
                  Second, you must check frequently the ShopItems. \n \
                  ShopItems lineup increase with your adventure deeper.  \n \
                  DarkWood's Boss <KingChar> is strong.  \n \
                  But you use a skill <Curse>, you can strike <KingChar>!")
    elif st.session_state["Player"].Lv == 2:
        st.write("In DoomsCave, it appear that <TrickFlower>.  \n \
                  Careful the <TrickFlower>'s skills.  \n \
                  If you dead, don't give up.  \n \
                  First, prepare the equipment at the Shop,  \n \
                  and collect Equipment in first half of Battle Stage!")
    elif st.session_state["Player"].Lv == 3:
        st.write("RuinFortless's Boss <HellChar> has a strongest skill <Swings>.  \n \
                  But, <HellChar>'s HP is Lower,  \n \
                  You must take an agressive offence, rush! rush! rush!")
    elif st.session_state["Player"].Lv == 4:
        st.write("EvilCastle's Boss <LordChar> use Magic Fire attack's.  \n \
                  You must prepare those magic attack's.")
    elif st.session_state["Player"].Lv == 5:
        st.write("Abyss's Boss <AbyssChar> has a skill <Curse>.  \n \
                  You must think about Strategy those attack.")
    else:
        st.write("You did a Great job!")
    st.button("Return", on_click = stM.change_Town)