import random
import math

class CharacterStatus():
    def __init__(self, name, Lv, HP, MP, Atk1, Atk2, Atk3, Def, STR, INT, VIT, MGR, Stat, Rew, gold, gacha1, gacha2):
        self.name = name
        self.Lv = Lv
        self.MaxHP = HP
        self.HP = HP
        self.MaxMP = MP
        self.MP = MP
        self.Atk1 = Atk1
        self.Atk2 = Atk2
        self.Atk3 = Atk3
        self.Def = Def
        self.STR = STR
        self.VIT = VIT
        self.INT = INT
        self.MGR = MGR
        #self.Equips = {"Weapon":"none", "Armor":"none", "Accesory":"none"}
        self.Status = Stat
        self.Rew = Rew
        self.gold = gold
        self.gacha1 = gacha1
        self.gacha2 = gacha2

    def Battle_Attack(self, Enemy, Flag):
        Sel = DiceRoll(1, 10)
        text = ""
        if Flag == True and "Aura!" in Enemy.Status:
            text = "AuraGuard first attack!"
            return text
        elif Sel == 1 and "Aura!" in Enemy.Status:
            text = "AuraGuard!"
            return text    
        AttackVal = DiceRoll(self.Atk1, self.Atk2) + self.Atk3
        CritMsg = ""
        if "Critical" in self.Status:
            Sel = DiceRoll(1,4)
            if Sel == 1:
                AttackVal = AttackVal * 2
                CritMsg = "Critical "
        if "ZANTETSU!!" in self.Status:
            SN = "ZANTETSU Attack"
            DmgVal = int((AttackVal))
        else:
            SN = "Attack"
            DmgVal = int((AttackVal - Enemy.Def) * (1 - Enemy.VIT/100))
        if "Immortal" in Enemy.Status:
            DmgVal = int(DmgVal / 2)
        if DmgVal < 1:
            text = f"{self.name} is {SN}! {Enemy.name} is defended!"
        else:
            Enemy.HP -= DmgVal
            text = f"{self.name} is {CritMsg}Attack! {DmgVal} Damage!"
            if Enemy.HP < 1:
                Enemy.HP = 0
        return text

    def Battle_MultiAttack(self, Enemy, RedM, ANum, Flag):
        if self.MP < RedM:
            text = f"{self.name} MP is not enough!"
            return text
        else:
            self.MP -= RedM 
            text = ""          
            for x in range(1, ANum + 1):
                text += self.Battle_Attack(Enemy, Flag) + "  \n"
            return text

    def Battle_Healing(self, RedM, Dice1, Dice2, Lv, PotionFlag):
        if self.MP < RedM:
            text = f"{self.name} MP is not enough!"
            return text
        else:
            self.MP -= RedM
            if PotionFlag == False:
                Healval = int(DiceRoll(Dice1, Dice2) * Lv * (1 + (self.INT/100)))
                text = f"{self.name} Cast a Healing! {Healval} Heal!"
            else:
                Healval = int(DiceRoll(Dice1, Dice2) * Lv)
                text = f"{self.name} {Healval} Healing!"
            if (Healval + self.HP) > self.MaxHP:
                self.HP = self.MaxHP
            else:
                self.HP += Healval
            return text

    def Battle_MPing(self, RedM, Dice1, Dice2, Lv, PotionFlag):
        if self.MP < RedM:
            text = f"{self.name} MP is not enough!"
            return text
        else:
            self.MP -= RedM
            Healval = DiceRoll(Dice1, Dice2)
            if (Healval + self.MP) > self.MaxMP:
                self.MP = self.MaxMP
            else:
                self.MP += Healval
            if PotionFlag == False:
                text = f"{self.name} Cast a MPing! {Healval} MP!"
            else:
                text = f"{self.name} {Healval} MPing!"
            return text

    def Battle_FireBall(self, Enemy, RedM, Dice1, Dice2, Lv, InfFlag):
        if self.MP < RedM:
            text = f"{self.name} MP is not enough!"
        else:
            self.MP -= RedM
            Fireval = int((DiceRoll(Dice1, Dice2) * Lv) * (1 + (self.INT/100)) * (1 - (Enemy.MGR/100)))
            if InfFlag == False:
                SN = "FireBall"
            else:
                SN = "Inferno"
            text = f"{self.name} Cast a {SN}! {Fireval} Damage!"
            Enemy.HP -= Fireval
            if Enemy.HP < 1:
                Enemy.HP = 0
        return text
    
    def Battle_Curse(self, Enemy, RedM, cur1_1, cur1_2, cur2_1, cur2_2, Lv):
        if self.MP < RedM:
            text = f"{self.name} MP is not enough!"
        else:
            self.MP -= RedM
            Reduceval1 = 0
            for x in range(Lv):
                Reduceval1 += int(DiceRoll(cur1_1, cur1_2) * (1 + (self.INT/100)) * 0.8) 
            if Enemy.Def < Reduceval1:
                Enemy.Def = 0
            else:
                Enemy.Def -= Reduceval1
            Reduceval2 = 0
            for x in range(Lv):
                Reduceval2 += int(DiceRoll(cur2_1, cur2_2) * (1 + (self.INT/100)) *0.8)        
            if Enemy.Atk2 <= Reduceval2:
                Enemy.Atk2 = 1
            else:
                Enemy.Atk2 -= Reduceval2
            text = f"{self.name} Cast Curse! {Enemy.name} is -{Reduceval1}Def! -{Reduceval2}Atk!"
        return text

    def Battle_Barrier(self, RedM, BNum):
        if self.MP < RedM:
            text = f"{self.name} MP is not enough!"
        else:
            self.MP -= RedM
            self.MGR += BNum
            if self.MGR > 100:
                self.MGR = 100
            text = f"{self.name} Cast a Barrier! MGR is {BNum} up!"
        return text  

class PlayerStatus(CharacterStatus):
    def __init__(self, name, Lv, HP, MP, Atk1, Atk2, Atk3, Def, STR, INT, VIT, MGR, Stat, Rew, gold, gacha1, gacha2):
        CharacterStatus.__init__(self, name, Lv, HP, MP, Atk1, Atk2, Atk3, Def, STR, INT, VIT, MGR, Stat, Rew, gold, gacha1, gacha2)
        if "!3" in name:
            Accesory = AccesoryStatus("Ring", 3, "", ['','',''])
        elif "!4" in name:
            Accesory = AccesoryStatus("Ring", 4, "", ['','','',''])
        elif "!5" in name:
            Accesory = AccesoryStatus("Ring", 5, "", ['','','','',''])
        elif "!6" in name:
            Accesory = AccesoryStatus("Ring", 5, "", ['','','','',''])
        elif "!7" in name:
            Accesory = AccesoryStatus("Ring", 5, "", ['','','','',''])
        elif "!8" in name:
            Accesory = AccesoryStatus("Ring", 5, "", ['','','','',''])
        else:
            Accesory = AccesoryStatus("Ring", 1, "", [''])
        if "Saikyo" in name:
            Weapon = WeaponStatus("Dagger", 20, 99, 0, 0, "Slash!!", [])
            Armor = ArmorStatus("Cloth", 9999, 0, 0, "Immortal!!", [])
            Accesory = AccesoryStatus("Ring", 1, "ZANTETSU!!", [''])
        else:
            Weapon = WeaponStatus("Dagger", 2, 6, 0, 0, "", [])
            Armor = ArmorStatus("Cloth", 1, 0, 0, "", [])
        self.Equips = {"Weapon":"none", "Armor":"none", "Accesory":"none"}
        self.Equip(Weapon, Armor, Accesory)
        
    def StatusInit(self):
        Weapon = WeaponStatus("Dagger", 2, 6, 0, 0, "", [])
        Armor = ArmorStatus("Cloth", 1, 0, 0, "", [])
        self.Equip(Weapon, Armor, self.Accesory)      

    def LevelUP(self, HP, MP):
        self.MaxHP += HP
        self.HP += HP
        self.MaxMP += MP
        self.MP += MP

    def Reflesh(self):    
        self.HP = self.MaxHP
        self.MP = self.MaxMP

    def Equip(self, Weapon, Armor, Accesory):
        self.Weapon = Weapon
        if self.Weapon.status != "":
            staval1 = " of " + self.Weapon.status
        else:
            staval1 = ""
        if self.Weapon.enum > 0:
            staval2 = " +" + str(self.Weapon.enum)
        else:
            staval2 = ""
        self.Equips["Weapon"] = self.Weapon.name + staval1 + staval2
        self.Armor = Armor
        if self.Armor.status != "":
            staval1 = " of " + self.Armor.status
        else:
            staval1 = ""
        if self.Armor.enum > 0:
            staval2 = " +" + str(self.Armor.enum)
        else:
            staval2 = ""        
        self.Equips["Armor"] = self.Armor.name + staval1 + staval2
        self.Accesory  = Accesory
        if self.Accesory.status != "":
            staval1 = " of " + self.Accesory.status
        else:
            staval1 = ""    
        self.Equips["Accesory"] = self.Accesory.name + staval1
        self.CalcBattleStatus()

    def CalcBattleStatus(self):
        self.Atk1 = self.Weapon.Atk1
        self.Atk2 = self.Weapon.Atk2
        self.Atk3 = self.Weapon.Atk3
        self.Def = self.Armor.def1 + self.Armor.def2
        self.STR = 0
        self.VIT = 0
        self.INT = 0
        self.MGR = self.Armor.MGR
        self.Status = []
        if self.Weapon.status != "":
            if self.Weapon.status in self.Status:
                pass
            else:
                self.Status.append(self.Weapon.status)
        if self.Armor.status != "":
            if self.Armor.status in self.Status:
                pass
            else:
                self.Status.append(self.Armor.status)
        if self.Accesory.status != "":
            if self.Accesory.status in self.Status:
                pass
            else:
                self.Status.append(self.Accesory.status)
        for x in self.Weapon.instatus:
            if "STR" in x:
                self.STR += int(x.replace("STR", ""))
            elif "INT" in x:
                self.INT += int(x.replace("INT", ""))
            elif "VIT" in x:
                self.VIT += int(x.replace("VIT", ""))
            elif "MGR" in x:
                self.MGR += int(x.replace("MGR", ""))
            else:
                pass            
        for x in self.Armor.instatus:
            if "STR" in x:
                self.STR += int(x.replace("STR", ""))
            elif "INT" in x:
                self.INT += int(x.replace("INT", ""))
            elif "VIT" in x:
                self.VIT += int(x.replace("VIT", ""))
            elif "MGR" in x:
                self.MGR += int(x.replace("MGR", ""))
            else:
                pass
        for x in self.Accesory.instatus:
            if "STR" in x:
                self.STR += int(x.replace("STR", ""))
            elif "INT" in x:
                self.INT += int(x.replace("INT", ""))
            elif "VIT" in x:
                self.VIT += int(x.replace("VIT", ""))
            elif "MGR" in x:
                self.MGR += int(x.replace("MGR", ""))
            else:
                pass
        self.Atk2 = math.ceil(self.Atk2 * (1+self.STR/100))
        if "Power" in self.Status:
            self.Atk1 += 2
        if self.MGR > 100:
            self.MGR = 100
        if self.VIT > 100:
            self.VIT = 100

class ItemStatus():
    def __init__(self, name, slot, status, instatus):
        self.name = name
        self.slot = slot
        self.status = status
        self.instatus = instatus
        self.enum = 0

    def AddSlot(self):
        self.slot += 1
        self.instatus.append("")

    def AddInstatus(self, slot, instatus):
        self.instatus[slot-1] = instatus

    def AddStatus(self, Status):
        self.status = Status

class WeaponStatus(ItemStatus):
    def __init__(self, name, Atk1, Atk2, Atk3, slot, status, instatus):
        self.Atk1 = Atk1
        self.Atk2 = Atk2
        self.Atk3 = Atk3
        self.species = "Weapon"
        self.score = int(Atk1 * Atk2)
        ItemStatus.__init__(self, name, slot, status, instatus)

    def AddEnchant(self, val):
        self.enum += 1
        self.Atk3 += val

class ArmorStatus(ItemStatus):
    def __init__(self, name, Defv, MGR, slot, status, instatus):
        self.def1 = Defv
        self.def2 = 0
        self.MGR = MGR
        self.species = "Armor"
        if "Uniqlo" in name:
            self.score = 400
        else:
            self.score = Defv + int(MGR//5)
        ItemStatus.__init__(self, name, slot, status, instatus)

    def AddEnchant(self, val, MGR):
        self.enum += 1
        self.def2 += val
        self.MGR += MGR
        
class AccesoryStatus(ItemStatus):
    def __init__(self, name, slot, status, instatus):
        self.species = "Accesory"
        ItemStatus.__init__(self, name, slot, status, instatus)

class ScrollStatus(ItemStatus):
    def __init__(self, status):
        self.species = "Scroll"
        name = "Scroll of " + status
        ItemStatus.__init__(self, name, 0, status, [])

class CrystalStatus(ItemStatus):
    def __init__(self, status):
        self.species = "Crystal"
        name = "Crystal of " + status
        ItemStatus.__init__(self, name, 0, status, [])

class BFStatus():
    def __init__(self, StageName, Mag, Rew, cnt):
        self.StageName = StageName
        self.Mag = Mag
        self.Rew = Rew
        self.cnt = cnt

class EnemyStatus():
    def __init__(self, StageName, Mag, cnt):
        Sel = DiceRoll(1,100)
        if StageName == "DarkWood" and cnt == 10:
            #KingCharl
            name = "KingChar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 20
            Atk1 = int(4 + (Mag - 1))
            Atk2 = int((DiceRoll(2,8)  + cnt ) * Mag)
            Atk3 = int(5 * Mag)
            Defval = int(((DiceRoll(2,int(Mag+4))  + (cnt//2) + 1)) * Mag)
            STR = 25
            INT = 0
            VIT = 25
            MGR = 0
            Status = []         
            gold = int(DiceRoll(2, 10) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "DoomsCave" and cnt == 10:
            #BloodChar
            name = "Bloodchar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 20
            Atk1 = int(4 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag)
            Atk3 = int(5 * Mag)
            Defval = int(((DiceRoll(4,int(Mag+8)) + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 0
            VIT = 20
            MGR = 0
            Status = ['Critical']          
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "RuinFortless" and cnt == 10:
            #HellChar
            name = "Hellchar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((30 + DiceRoll(cnt, 12)) * Mag)
            MP = 40
            Atk1 = int(3 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag * 0.8)
            Atk3 = int(5 * Mag)
            Defval = int(((DiceRoll(2,int(Mag+2)) + (cnt//2) + 1)) * Mag * 0.7)
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = ["Swings!"]          
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "EvilCastle" and cnt == 10:
            #LordChar
            name = "LordChar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 100
            Atk1 = int(4 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag)
            Atk3 = int(5 * Mag)
            Defval = int(((DiceRoll(2,int(Mag+6)) + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 25
            VIT = 0
            MGR = 99
            Status = ["Fire"]          
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "Abyss" and cnt == 10:
            #AbyssChar
            name = "AbyssChar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 40
            Atk1 = int(4 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag)
            Atk3 = int(5 * Mag)
            Defval = int(((DiceRoll(2,int(Mag+8)) + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 30
            VIT = 50
            MGR = 0
            Status = ["Curse!"]          
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "ChaosePlane" and cnt == 10:
            #ChaoseChar
            name = "ChaoseChar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 40
            Atk1 = int(4 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag)
            Atk3 = int(5 * Mag)
            Defval = int(((DiceRoll(10,int(Mag+8)) + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 50
            VIT = 50
            MGR = 99
            Status = ["Fire"]          
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "YAMATO" and cnt == 10:
            #BushidoChar
            name = "BushidoChar(StageBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 40
            Atk1 = int(4 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag)
            Atk3 = int(10 * Mag)
            Defval = int(((DiceRoll(2,int(Mag+8)) + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 50
            VIT = 70
            MGR = 70
            Status = ["Swings!", "Critical", "Fire"]          
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 2
            gacha1 = 0
            gacha2 = 7
        elif StageName == "Vhalhara" and cnt == 10:
            #OdenChar
            name = "OdenChar(LastBoss)"
            Lv = int(2 + Mag)
            HP = int((60 + DiceRoll(cnt, 16)) * Mag)
            MP = 40
            Atk1 = int(4 + int((Mag - 1)))
            Atk2 = int((DiceRoll(2,8) + cnt ) * Mag)
            Atk3 = int(10 * Mag)
            Defval = int(((DiceRoll(4,int(Mag+8)) + (cnt//2) + 1)) * Mag)
            STR = 20
            INT = 50
            VIT = 80
            MGR = 80
            Status = ["Power","Curse!","Fire"]   
            gold = int(DiceRoll(3, 6) * Mag)
            MonRew = 4
            gacha1 = 0
            gacha2 = 7
        elif cnt == 5:
            #MiddleBoss
            name = "GigaChar(Boss)"
            Lv = int(3 + Mag)
            HP = int((50 + DiceRoll(cnt, 16)) * Mag)
            MP = 20
            Atk1 = int(3 + (Mag - 1))
            Atk2 = int((DiceRoll(2,8)  + cnt ) * Mag)
            Atk3 = int(cnt//3 * Mag)
            Defval = int(((DiceRoll(1,int(Mag+8))  + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = []         
            gold = int(DiceRoll(2, 10) * Mag)
            MonRew = 1
            gacha1 = 3
            gacha2 = 2
        elif Sel > 80:
            #GigaChar
            name = "GigaChar"
            Lv = int(2 + Mag)
            HP = int((40 + DiceRoll(cnt, 16)) * Mag)
            MP = 20
            Atk1 = int(3 + (Mag - 1))
            Atk2 = int((DiceRoll(2,8)  + cnt ) * Mag)
            Atk3 = int(cnt//4 * Mag)
            Defval = int(((DiceRoll(1,int(Mag+8))  + (cnt//2) + 1)) * Mag)
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = []         
            gold = int(DiceRoll(1, 10) * Mag)
            MonRew = 1
            gacha1 = 2
            gacha2 = 0                       
        elif Sel > 60 and StageName != "DarkWood":
            #TrickFlower
            name = "TrickFlower"
            Lv = int(1 + Mag)
            HP = int((30 + DiceRoll(cnt, 6)) * Mag)
            MP = 40
            Atk1 = int(2 + (Mag - 1))
            Atk2 = int((DiceRoll(2,6) + cnt) * Mag)
            Atk3 = int(cnt//5 * Mag)
            Defval = int(((DiceRoll(1,int(4+Mag)) + (cnt//2))) * Mag)
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = []
            Sel = DiceRoll(1,3)
            if Sel == 1:
                Status.append('Fire')
            Sel = DiceRoll(1,3)
            if Sel == 1:
                Status.append('Curse!')
            Sel = DiceRoll(1,3)
            if Sel == 1:
                Status.append('Swings!')
            gold = int(DiceRoll(1, 8) * Mag)
            MonRew = 1
            gacha1 = 2
            gacha2 = 0
        elif (Sel > 60 and StageName == "DarkWood") or (Sel > 40 and StageName != "DarkWood"):
            #SharmanChar
            name = "SharmanChar"
            Lv = int(1 + Mag)
            HP = int((30 + DiceRoll(cnt, 8)) * Mag)
            MP = 40
            Atk1 = int(2 + (Mag - 1))
            Atk2 = int((DiceRoll(2,4) + cnt) * Mag)
            Atk3 = int(cnt//5 * Mag)
            Defval = int(((DiceRoll(1,int(4+Mag)) + (cnt//2))) * Mag)
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = []
            gold = int(DiceRoll(1,6) * Mag)
            MonRew = 0
            gacha1 = 1
            gacha2 = 0       
        elif Sel > 5:
            #HillChar
            name = "HillChar"
            Lv = int(1 + Mag)
            HP = int((20 + DiceRoll(cnt, 8)) * Mag)
            MP = 20
            Atk1 = int(2 + (Mag - 1))
            Atk2 = int((DiceRoll(2,4) + cnt) * Mag)
            Atk3 = int(cnt//5 * Mag)
            Defval = int(((DiceRoll(1,int(4+Mag)) + (cnt//2))) * Mag)
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = []
            gold = int(DiceRoll(1,4) * Mag)
            MonRew = 0
            gacha1 = 1
            gacha2 = 0
        else:
            #RuinGuardian
            name = "RuinGuardian"
            Lv = int(3 + Mag)
            HP = int(120 * Mag)
            MP = 20
            Atk1 = 1
            Atk2 = int(40 * Mag)
            Atk3 = 0
            if StageName != "DarkWood":
                Defval = int(30 * int(Mag-1))
            else:
                Defval = 10
            STR = 0
            INT = 0
            VIT = 0
            MGR = 0
            Status = []
            gold = int(40 * Mag)
            MonRew = 3
            gacha1 = 0
            gacha2 = 8
        self.Enemy = CharacterStatus(name,Lv,HP,MP,Atk1,Atk2,Atk3,Defval,STR, INT, VIT, MGR, Status, MonRew, gold, gacha1, gacha2)

    def Enemy_Attack(self, Player, AuraFlag):
        EnemyAction = DiceRoll(1,5)
        if self.Enemy.name == "HillChar":
            if EnemyAction == 5:
                text = self.Enemy.Battle_FireBall(Player, 4, 2, 8, self.Enemy.Lv, False)
            else:
                text = self.Enemy.Battle_Attack(Player, AuraFlag)
        elif self.Enemy.name == "SharmanChar"  or self.Enemy.name == "LordChar":
            text1 = ""; text2 = ""  
            if EnemyAction == 5 or EnemyAction == 4: 
                text1 = self.Enemy.Battle_FireBall(Player, 8, 2, 10, self.Enemy.Lv, False)
            elif EnemyAction == 3:
                text1 = self.Enemy.Battle_Healing(6, 3, 10, self.Enemy.Lv, False)
            elif EnemyAction == 2:
                text1 = self.Enemy.Battle_MultiAttack(Player, 4, 2, AuraFlag)
                if "Fire" in self.Enemy.Status:
                    text2 = self.Enemy.Battle_FireBall(Player, 0, 2, 6, self.Enemy.Lv, False)
                else:
                    text2 = ""
            else:
                text1 = self.Enemy.Battle_Attack(Player, AuraFlag)
                if "Fire" in self.Enemy.Status:
                    text2 = self.Enemy.Battle_FireBall(Player, 0, 2, 6, self.Enemy.Lv, False)
                else:
                    text2 = ""
            if text2 != "":
                text1 += "  \n"
            text = text1 + text2
        elif self.Enemy.name == "RuinGuardian":
            if EnemyAction == 5:
                text = self.Enemy.Battle_Healing(6, 3, 10, self.Enemy.Lv, False)
            else:
                text = self.Enemy.Battle_Attack(Player, AuraFlag)            
        else:
            text1 = ""; text2 = ""; text3 = ""
            if "Swings!" in self.Enemy.Status:
                text1 = self.Enemy.Battle_MultiAttack(Player, 0, 2, AuraFlag)
            else:
                text1 = self.Enemy.Battle_Attack(Player, AuraFlag)
            if "Fire" in self.Enemy.Status:
                text2 = self.Enemy.Battle_FireBall(Player, 0, 2, 6, self.Enemy.Lv, False)
            else:
                text2 = ""
            if "Curse!" in self.Enemy.Status:
                text3 = self.Enemy.Battle_Curse(Player, 0, 1, 6, 1, 6, self.Enemy.Lv)
            else:
                text3 = ""
            if text2 != "" or text3 != "":
                text1 += "  \n"
            if text3 != "" and text2 != "":
                text2 += "  \n"
            text = text1 + text2 + text3
        return text

def DiceRoll(d1, d2):
    val = 0
    for x in range(1, d1+1):
        val += random.randint(1, d2)
    return val


