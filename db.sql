CREATE TABLE IF NOT EXISTS quest (
  QuestID int AUTO_INCREMENT,
  Name varchar(25) NOT NULL,
  ShortName varchar(50) NOT NULL,
  CONSTRAINT quest_pk PRIMARY KEY (QuestID)
);
CREATE UNIQUE INDEX quest_ShortName_uindex ON quest (ShortName);

CREATE TABLE IF NOT EXISTS stage
(
	StageID int AUTO_INCREMENT,
	Progress int(4) NULL,
	LogText text NULL,
	RewardExperience int NULL,
	FinishesQuest bool DEFAULT false NULL,
	ShortName int NULL,
	CONSTRAINT stage_pk PRIMARY KEY (StageID),
	CONSTRAINT Stage_Quest_fk FOREIGN KEY (ShortName) REFERENCES quest (ShortName)
);

-- CREATE TABLE monster (
--     monsterID int(5) NOT NULL AUTO_INCREMENT,
--     monsterName varchar(50) NOT NULL,
--     monsterFriendlyName varchar(50) NOT NULL,
--     maxHP int,
--     maxAP int,
--     monsterClass char(25),
--     droplistID char(50),
--     attackCost int,
--     attackChance int,
--     criticalSkill int,
--     criticalMultiplier decimal(2,1),
--     blockChance int,
--     damageResistance int,
--     unique boolean,
--     phraseID varchar(50),
--     movementAggressionType varhcar(50),
--     faction varchar(50),
--     UNIQUE KEY (monsterID)
-- )