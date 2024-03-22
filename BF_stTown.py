import streamlit as st
import BF_stMain as stM
import BF_ObjectDef as OB
import PCommand as PC

def ca():
    st.session_state["page_control"] = 3

def ea():
    st.session_state["page_control"] = 4

def change_BFinit(BF):
    st.session_state["BF"] = BF
    st.session_state["ShopList"] = []
    st.session_state["page_control"] = 5

def Town_command():
    st.button("Town Shop", on_click = stM.change_Shop)
    st.button("Town Enchant", on_click = stM.change_Enchant)
    st.button("Town AddSlot", on_click = ca)
    st.button("Town Elder Advice", on_click = ea)
    BF1 = "BF " + st.session_state["BF1"].StageName
    BF2 = "BF " + st.session_state["BF2"].StageName
    if BF1 != "BF none":
        st.button(BF1, on_click = change_BFinit, args = [st.session_state["BF1"]])
    if BF2 != "BF none":
        st.button(BF2, on_click = change_BFinit, args = [st.session_state["BF2"]])

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
    elif x.species == "Armor":
        st.session_state["NewArmor"] = x
        st.session_state["page_control"] = 12    
    elif x.species == "Scroll":
        st.session_state["NewScroll"] = x
        st.session_state["page_control"] = 13
    elif x.species == "Crystal":
        st.session_state["NewCrystal"] = x
        st.session_state["page_control"] = 14
    else:
        st.write("Irregal Item")

def Town_DispPStatus():
    st.sidebar.header("BF 1.2")
    text = PC.DispPlayerStatus(st.session_state["Player"], True)
    st.sidebar.markdown(text)

def Town():
    st.session_state["Player"].CalcBattleStatus()
    Town_DispPStatus()
    st.subheader("Town")
    Town_command()

def Shop():
    Town_DispPStatus()
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
    #st.button("Town", on_click = stM.change_Town)
    st.button("Return", on_click = stM.change_Town)
        
def Enchant_Weapon():
    if st.session_state.WEcost[0] == 9999:
        st.write("Your Weapon is Max Enchanted!")
    elif st.session_state["Player"].gold > (st.session_state.WEcost[0] - 1):
        EVal = st.session_state.WEcost[1]
        st.write(f"Weapon is enchanted! +{EVal}")
        st.session_state["Player"].gold -= st.session_state.WEcost[0]
        st.session_state["Player"].Weapon.AddEnchant(EVal)
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory)
    else:
        st.write("You have not enogh money!")
    Town_DispPStatus()
    st.button("Return", on_click = stM.change_Enchant)

def Enchant_Armor():
    if st.session_state.AEcost[0] == 9999:
        st.write("Your Armor is Max Enchanted!")
    elif st.session_state["Player"].gold > (st.session_state.AEcost[0] - 1):
        EVal = st.session_state.AEcost[1]
        MGRVal = st.session_state.AEcost[2]
        st.write(f"Armor is enchanted! Def +{EVal}")
        st.write(f"Armor is enchanted! MGR +{MGRVal}")
        st.session_state["Player"].gold -= st.session_state.AEcost[0]
        st.session_state["Player"].Armor.AddEnchant(EVal, MGRVal)
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory)
    else:
        st.write("You have not enogh money!")
    Town_DispPStatus()
    st.button("Return", on_click = stM.change_Enchant)

def change_Enchant_Weapon():
    st.session_state["page_control"] = 21

def change_Enchant_Armor():
    st.session_state["page_control"] = 22

def Enchant():
    Town_DispPStatus()
    st.subheader("Enchant Workshop")    
    st.write("Select Enchant for ")
    WVal = st.session_state["Player"].Weapon.enum
    if WVal > 4:
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
    if st.session_state["Player"].Weapon.slot > 0:
        st.write("Your Weapon Slot is Max!")
    elif st.session_state["Player"].gold > 200:
        st.write("Add Slot Weapon +1!")
        st.session_state["Player"].gold -= 200
        st.session_state["Player"].Weapon.AddSlot()
    else:
        st.write("You have not enogh gold!")
    Town_DispPStatus()
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
    Town_DispPStatus()
    st.button("Return", on_click = ca)

def change_AddSlot_Weapon():
    st.session_state["page_control"] = 31

def change_AddSlot_Armor():
    st.session_state["page_control"] = 32

def AddSlot():
    Town_DispPStatus()
    st.subheader("AddSlot Workshop") 
    st.write("Max Equip Slot is 1.")
    st.write("Add Slot cost is 200 gold.")    
    st.write("Select Enchant for ") 
    st.button("Weapon", on_click = change_AddSlot_Weapon)
    st.button("Armor", on_click = change_AddSlot_Armor)
    st.button("Return", on_click = stM.change_Town)

def change_Ending01():
    st.session_state["page_control"] = 6

def change_Ending02():
    st.session_state["page_control"] = 61

def change_Ending03():
    st.session_state["page_control"] = 62

def ElderAdvice():
    Town_DispPStatus()
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
    elif st.session_state["Player"].Lv == 6:
        st.button("老人の話を聞く", on_click = change_Ending01)
        st.session_state["Player"].Lv = 7
    elif st.session_state["Player"].Lv == 7:
        st.write("You did a Great job!")
    else:
        st.write("Elder error")
    st.button("Return", on_click = stM.change_Town)

def Ending01():
    st.write("老人はあなたの姿を見るなり勢い良くしゃべり始めた。  \n")
    st.write("「よくここまでたどり着けたな。  \n")
    st.write("　楽しめたか？」  \n")
    st.write("　老人はにやにやとあなたの表情を吟味しながら続けた。  \n")
    st.write("「楽しめないはずがあるまい。楽しかったからここまでこれたはずだ。  \n")
    st.write("　では問おう。何が楽しかった？」  \n")
    st.write("　困惑したあなたに老人は語り掛け続けた。  \n")
    st.write("「分らんのか。では教えてやろう。」  \n")
    st.write("　老人は背筋を伸ばしオペラ歌手のように両手を広げ、満面の笑みを浮かべた。  \n")
    st.write("「教えてやろう！お前は何が楽しかったのか！  \n")
    st.write("　たったの一言で言い表せる。このゲームの楽しみの全てを！」  \n")
    st.button("OK", on_click = change_Ending02)

def Ending02():
    st.subheader("2d6  \n")
    st.write("   \n")
    st.write("「2d6だ！2d6、それがこのゲームの楽しみの全てだ！  \n")
    st.write("　2d6を振る！12が出る！脳汁が出る。これが全てだ。この世界の源泉だ！  \n")
    st.write("　おまえはここに至るまで無数の2d6を振り続けてきた。  \n")
    st.write("　そう、振り続けてきた。12が出ることを期待してな。  \n")
    st.write("　12が出た瞬間、お前から噴き出る脳汁でわしは溺死しそうになったわいｗ  \n") 
    st.write("   \n")  
    st.write("　期待。これ以上の娯楽はこの世にない。  \n")
    st.write("　人間は進化し続け、いずれ肉体を捨て、精神だけの存在になる。  \n")
    st.write("　肉を捨て、肉からなる喜びを捨て去った後、人類は何を楽しみに生きるというのだ。  \n")
    st.write("　それが、期待だ！」  \n")
    st.button("OK", on_click = change_Ending03)

def Ending03():
    st.write("「2d6を振る。12が出ることを期待し、2d6を振る。  \n")
    st.write("　極上の楽しみだ。それ以外に世界に何が必要か！  \n")
    st.write("　希望を見失ったとき、楽しみを感じられなくなったとき、2d6を振るが良い！  \n")
    st.write("　2d6だ。2d6があればお前は末永く楽しく生きられる。  \n")
    st.write("　覚えておけ、そして唱えよ、2d6！」  \n")
    st.subheader("　2d6！　2d6！　2d6！  \n")
    st.write("   \n")
    st.write("End.   \n")
    st.button("OK", on_click = stM.change_Town)