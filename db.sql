-- CREATE TABLE quest (
--     questID int(5) NOT NULL AUTO_INCREMENT,
--     questShortName varchar(25) NOT NULL UNIQUE,
--     questName varchar(50) NOT NULL,
--     UNIQUE (questID, questShortName)
-- );

-- CREATE TABLE stage (
--     stageID int(5) NOT NULL AUTO_INCREMENT,
--     questShortName varchar(25) NOT NULL,
--     progress int(3),
--     logText text,
--     rewardExp int,
--     finishesQuest boolean,
--     UNIQUE KEY (stageID),
--     FOREIGN KEY (questShortName) REFERENCES quest(questShortName)
-- );

SELECT * FROM quest ORDER BY questID ASC;