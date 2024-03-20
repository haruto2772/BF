import streamlit as st
import BF_ObjectDef as OB
import PCommand as PC
import BF_stMain as stMain

def DispBFinfo():
    Stage = st.session_state["BF"].StageName
    cnt = st.session_state["BF"].cnt
    st.write(f"Stage: {Stage} <{cnt}>")    

def BFResult():
    DispBFinfo()
    stMain.DispEStatus()
    BF_DispPlayerComand()
    st.write(st.session_state["BFResult"])

def BFResult_PlayerWin():
    DispBFinfo()
    stMain.DispEStatus()
    BF_DispPlayerStatus()
    st.markdown(st.session_state["BFResult"]) 
    st.button("OK", key = "OK_BF01", on_click = change_BFBattleEnd)   

def BFResult_PlayerLose():
    DispBFinfo()
    stMain.DispEStatus()
    BF_DispPlayerStatus()
    st.markdown(st.session_state["BFResult"]) 
    st.button("OK", key = "OK_BF01", on_click = change_Deadend)       

def change_BFBattleEnd():
    Item = PC.GetShopItem(st.session_state["Enemy"].Enemy.Rew, \
                          st.session_state["BF"].Rew + st.session_state["Enemy"].Enemy.Rew + st.session_state["BF"].cnt, \
                          st.session_state["Player"], st.session_state["BF"].StageName)
    st.session_state["ShopList"].append(Item)
    st.session_state["page_control"] = 52

def change_Deadend():
    st.session_state["Player"].StatusInit()
    st.session_state["page_control"] = 0      

def LevelUP():
    LV1 = OB.DiceRoll(1, 4)
    LV2 = OB.DiceRoll(1, 2)
    st.session_state["Player"].LevelUP(LV1, LV2)
    return f"Level Up! HP +{LV1}, MP +{LV2}"

def BattleResult(text1):
    if st.session_state["Enemy"].Enemy.HP < 1:
        #Enemy Dead
        Enemyname = st.session_state["Enemy"].Enemy.name
        text2 = f"{Enemyname} is Dead!!"
        text2 = f"**:red[{text2}]**"
        text3 = ""
        gold = st.session_state["Enemy"].Enemy.gold
        st.session_state["Player"].gold += gold
        text4 = f"Get {gold} gold."
        Sel = OB.DiceRoll(1,5)
        if Sel == 5:
            text5 = LevelUP()
        else:
            text5 = ""
        if "Heal" in st.session_state["Player"].Status:
            text6 = st.session_state["Player"].Battle_Healing(0, st.session_state["Player"].Lv, 6, 1, True)
        else:
            text6 = ""
        if "Mana" in st.session_state["Player"].Status:
            text7 = st.session_state["Player"].Battle_MPing(0, st.session_state["Player"].Lv, 4, 1, True)
        else:
            text7 = ""
        if text6 != "" or text7 != "":
            text5 += "  \n"
        if text7 != "":
            text6 += "  \n"
        st.session_state["BFResult"] = text1 + "  \n" + text2 + "  \n" + text3 + "  \n" + text4 + "  \n" + text5 + text6 + text7
        st.session_state["page_control"] = 57
    else:
        text2 = st.session_state["Enemy"].Enemy_Attack(st.session_state["Player"], st.session_state.AuraFlag)
        if "Aura" in text2:
            st.session_state.AuraFlag = False
        if st.session_state["Player"].HP < 1:
            #Player Dead
            name = st.session_state["Player"].name
            text3 = f"*** {name} is Dead!! ***"
            text3 = f"**:red[{text3}]**"
            st.session_state["BFResult"] = text1 + "  \n" + text2 + "  \n" + text3
            st.session_state["page_control"] = 58
        else:
            #Battle Continue
            text3 = ""
            st.session_state["BFResult"] = text1 + "  \n" + text2 + "  \n" + text3
            st.session_state["page_control"] = 51

def BF_Attack():
    text1 = ""; text2 = "";text3 = "";
    if "Swings" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 0, 2, False)
    else:
        text1 = st.session_state["Player"].Battle_Attack(st.session_state["Enemy"].Enemy, False)
    if "Fire" in st.session_state["Player"].Status:
        text2 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 0, 2, 12, st.session_state["Player"].Lv) 
    else:
        text2 = ""
    if "Curse" in st.session_state["Player"].Status:
        text3 = st.session_state["Player"].Battle_Curse(st.session_state["Enemy"].Enemy, 0, 1, 4, 1, 4, st.session_state["Player"].Lv)
    else:
        text3 = ""
    if text2 != "" or text3 != "":
        text1 += "  \n"
    if text3 != "" and text2 != "":
        text2 += "  \n"
    BattleResult(text1 + text2 + text3)

def BF_WAttack():
    text1 = ""; text2 = "";text3 = "";
    text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 4, 2, False)
    if "Fire" in st.session_state["Player"].Status:
        text2 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 0, 2, 12, st.session_state["Player"].Lv) 
    else:
        text2 = ""
    if "Curse" in st.session_state["Player"].Status:
        text3 = st.session_state["Player"].Battle_Curse(st.session_state["Enemy"].Enemy, 0, 1, 4, 1, 4, st.session_state["Player"].Lv)
    else:
        text3 = ""
    if text2 != "" or text3 != "":
        text1 += "  \n"
    if text3 != "":
        text2 += "  \n"
    BattleResult(text1 + text2 + text3)

def BF_Healing():
    text1 = st.session_state["Player"].Battle_Healing(6, 3, 16, st.session_state["Player"].Lv, False)
    BattleResult(text1)

def BF_FireBall():
    text1 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 8, 3, 16, st.session_state["Player"].Lv)
    BattleResult(text1)

def BF_Curse():
    text1 = st.session_state["Player"].Battle_Curse(st.session_state["Enemy"].Enemy, 12, 2, 4, 2, 4, st.session_state["Player"].Lv)
    BattleResult(text1)

def BF_Barrier():
    text1 = st.session_state["Player"].Battle_Barrier(5, 30)
    BattleResult(text1)

def BF_DispPlayerStatus():
    stMain.DispPStatus()

def BF_DispPlayerComand():
    stMain.DispPStatus()
    st.sidebar.button("1.Attack", on_click = BF_Attack)
    st.sidebar.button("2.WAttack(4)", on_click = BF_WAttack)
    st.sidebar.button("3.Healing(6)", on_click = BF_Healing)
    st.sidebar.button("4.FireBall(8)", on_click = BF_FireBall)
    st.sidebar.button("5.Curse(12)", on_click = BF_Curse)
    st.sidebar.button("5.Barrier(5)", on_click = BF_Barrier)
    st.sidebar.button("7.Escape to Town", on_click = stMain.change_Town)

def BFinit():
    st.session_state["BF"].cnt += 1
    st.session_state.AuraFlag = True
    if st.session_state["BF"].cnt > 10:
        SName = st.session_state["BF"].StageName
        text = ""
        if st.session_state["Player"].Lv == 1 and st.session_state["BF"].StageName == "DarkWood" or \
            st.session_state["Player"].Lv == 2 and st.session_state["BF"].StageName == "DoomsCave" or \
            st.session_state["Player"].Lv == 3 and st.session_state["BF"].StageName == "RuinFortless" or \
            st.session_state["Player"].Lv == 4 and st.session_state["BF"].StageName == "EvilCastle" or \
            st.session_state["Player"].Lv == 5 and st.session_state["BF"].StageName == "Abyss":
            if st.session_state["BF"].StageName == "Abyss":
                text = "Conglaturations!! "
            st.session_state["Player"].Lv += 1
            st.write(f"** {text}Clear the {SName} **")
            st.session_state["Player"].Accesory.AddSlot()
            getgold = int(OB.DiceRoll(12,20) * st.session_state["BF"].Mag)
            st.session_state["Player"].gold += getgold
            st.write("Accesory Slot +1!")        
            st.write(f"Get {getgold} gold!")  
        else:
            st.write(f"Clear the {SName}")
        st.button("Return Town", on_click = stMain.change_Town)
    else:
        st.session_state["Enemy"] = OB.EnemyStatus(st.session_state["BF"].StageName, st.session_state["BF"].Mag, st.session_state["BF"].cnt)
        DispBFinfo()
        stMain.DispEStatus()
        BF_DispPlayerComand()
        EnemyName = st.session_state["Enemy"].Enemy.name
        st.write(f"{EnemyName} is appeared!!")

def Weapon_change():
    NewWeaponName = st.session_state["NewWeapon"].name
    #st.write(f"Equip a new {NewWeaponName}!")
    st.session_state["Player"].Equip(st.session_state["NewWeapon"], st.session_state["Player"].Armor, st.session_state["Player"].Accesory)   
    #st.session_state["page_control"] = 53

def Drop_Weapon():
    pass
    #st.write("Drop Weapon.")
    #st.session_state["page_control"] = 53

def Armor_change():
    NewArmorName = st.session_state["NewArmor"].name
    #st.write(f"Equip a new {NewArmorName}!")
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["NewArmor"], st.session_state["Player"].Accesory)   
    #st.session_state["page_control"] = 54

def Drop_Armor():
    pass
    #st.write("Drop Armor.")
    #st.session_state["page_control"] = 54

def Scroll_Weapon(status):
    st.session_state["Player"].Weapon.AddStatus(status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    #st.session_state["page_control"] = 55

def Scroll_Armor(status):
    st.session_state["Player"].Armor.AddStatus(status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    #st.session_state["page_control"] = 55

def Scroll_Accesory(status):
    st.session_state["Player"].Accesory.AddStatus(status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    #st.session_state["page_control"] = 55

def Drop_Scroll():
    pass
    #st.write("Drop Scroll.")
    #st.session_state["page_control"] = 55

def SelectWeapon():
    BF_DispPlayerStatus()
    #DispBFinfo()    
    st.write("You get a Weapon!")
    text1 = PC.DispWeaponStatus("New ; ", st.session_state["NewWeapon"], st.session_state["NewWeapon"].name)
    text2 = PC.DispWeaponStatus("Now ; ", st.session_state["Player"].Weapon, st.session_state["Player"].Equips["Weapon"])
    st.write(text1)
    st.write(text2)
    st.button("Exchange", key = "ExchangeWeapon", on_click=Weapon_change)
    st.button("Drop", on_click = Drop_Weapon) 

def GetWeapon():
    st.session_state["NewWeapon"] = PC.GetWeapon(st.session_state["BF"].cnt + st.session_state["BF"].Rew + st.session_state["Enemy"].Enemy.Rew, st.session_state["Player"])
    if st.session_state["NewWeapon"].score > st.session_state["Player"].Weapon.score * 0.95:
        SelectWeapon()
        st.session_state["page_control"] = 53
    else:
        GetArmor()

def SelectArmor():
    BF_DispPlayerStatus()
    #DispBFinfo()
    st.write("You get a Armor!")
    text3 = PC.DispArmorStatus("New ; ", st.session_state["NewArmor"], st.session_state["NewArmor"].name)
    text4 = PC.DispArmorStatus("Now ; ", st.session_state["Player"].Armor, st.session_state["Player"].Equips["Armor"])
    st.write(text3)
    st.write(text4)
    st.button("Exchange", key = "ExchangeArmor", on_click=Armor_change)
    st.button("Drop", on_click = Drop_Armor)
    
def GetArmor():
    st.session_state["NewArmor"] = PC.GetArmor(st.session_state["BF"].cnt + st.session_state["BF"].Rew + st.session_state["Enemy"].Enemy.Rew, st.session_state["Player"])
    if st.session_state["NewArmor"].score > st.session_state["Player"].Armor.score * 0.95:
        SelectArmor()
        st.session_state["page_control"] = 54
    else:
        GetScroll()

def SelectScroll():
    BF_DispPlayerStatus()
    #DispBFinfo()
    Scrollname = st.session_state["NewScroll"].status
    st.write(f"You get a Scroll of {Scrollname}!")
    st.button("Enchant Weapon", key = "Enchant Weapon", on_click=Scroll_Weapon, args=[st.session_state["NewScroll"].status])
    st.button("Enchant Armor", key = "Enchant Armor", on_click=Scroll_Armor, args=[st.session_state["NewScroll"].status])
    st.button("Enchant Accesory", key = "Enchant Accesory", on_click=Scroll_Accesory, args=[st.session_state["NewScroll"].status])
    st.button("Drop", on_click = Drop_Scroll)

def GetScroll():
    st.session_state["NewScroll"] = PC.GetScroll(st.session_state["Player"], st.session_state["Enemy"].Enemy.Rew, st.session_state["BF"].StageName)
    if st.session_state["NewScroll"].status != "none":
        SelectScroll()
        st.session_state["page_control"] = 55
    else:
        GetCrystal()

def change_Crystal_Weapon(BFFlag):
    if BFFlag == True:
        st.session_state["page_control"] = 551
    else:
        st.session_state["page_control"] = 554

def change_Crystal_Armor(BFFlag):
    if BFFlag == True:
        st.session_state["page_control"] = 552
    else:
        st.session_state["page_control"] = 555

def change_Crystal_Accesory(BFFlag):
    if BFFlag == True:
        st.session_state["page_control"] = 553
    else:
        st.session_state["page_control"] = 556

def Enchant_Crystal_Weapon(x, status):
    st.session_state["Player"].Weapon.AddInstatus(x, status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 

def Crystal_Weapon(page_control):
    BF_DispPlayerStatus()
    st.session_state["page_control"] = page_control
    stStr = st.session_state["NewCrystal"].name
    st.write(f"{stStr}")
    st.write("Select Weapon Slot.")
    for x in range(st.session_state["Player"].Weapon.slot):
        st.button(f"Slot{x+1}", key = x+1, on_click = Enchant_Crystal_Weapon, args = [x+1, st.session_state["NewCrystal"].status])
    st.button("Drop")

def Enchant_Crystal_Armor(x, status):
    st.session_state["Player"].Armor.AddInstatus(x, status)
    st.session_state["Player"].Equip(st.session_state["Player"].Armor, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 

def Crystal_Armor(page_control):
    BF_DispPlayerStatus()
    st.session_state["page_control"] = page_control
    stStr = st.session_state["NewCrystal"].name
    st.write(f"{stStr}")
    st.write("Select Armor Slot.")
    for x in range(st.session_state["Player"].Armor.slot):
        st.button(f"Slot{x+1}", key = x+1, on_click = Enchant_Crystal_Armor, args = [x+1, st.session_state["NewCrystal"].status])
    st.button("Drop")

def Enchant_Crystal_Accesory(x, status):
    st.session_state["Player"].Accesory.AddInstatus(x, status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    
def Crystal_Accesory(page_control):
    BF_DispPlayerStatus()
    st.session_state["page_control"] = page_control
    stStr = st.session_state["NewCrystal"].name
    st.write(f"{stStr}")
    st.write("Select Accesory Slot.")
    for x in range(st.session_state["Player"].Accesory.slot):
        st.button(f"Slot{x+1}", key = x+1, on_click = Enchant_Crystal_Accesory, args = [x+1, st.session_state["NewCrystal"].status])
    st.button("Drop")

def Drop_Crystal(BFFlag):
    #st.write("Drop Crystal!")
    if BFFlag == True:
        st.session_state["page_control"] = 50
    else:
        st.session_state["page_control"] = 1
    #st.session_state["page_control"] = 50

def SelectCrystal(BFFlag):
    BF_DispPlayerStatus()
    #DispBFinfo()
    Crystalname = st.session_state["NewCrystal"].status
    st.write(f"You get a Crystal of {Crystalname}!")
    if st.session_state["Player"].Weapon.slot > 0:
        if st.session_state["Player"].Armor.slot > 0:
            st.button("Enchant Weapon", key = "Enchant Weapon", on_click=change_Crystal_Weapon, args=[BFFlag])
            st.button("Enchant Armor", key = "Enchant Armor", on_click=change_Crystal_Armor, args=[BFFlag])
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
        else:
            st.button("Enchant Weapon", key = "Enchant Weapon", on_click=change_Crystal_Weapon, args=[BFFlag])
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
    else:
        if st.session_state["Player"].Armor.slot > 0:
            st.button("Enchant Armor", key = "Enchant Armor", on_click=change_Crystal_Armor, args=[BFFlag])
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
        else:
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
    st.button("Drop", on_click = Drop_Crystal, args=[BFFlag])    

def GetCrystal():
    st.session_state["NewCrystal"] = PC.GetCrystal(st.session_state["Player"], st.session_state["Enemy"].Enemy.Rew, st.session_state["BF"].StageName)
    if st.session_state["NewCrystal"].status != "none0":
        SelectCrystal(True)      
    else:
        BFinit()