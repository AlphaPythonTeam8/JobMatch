
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
SHOW WARNINGS;
-- -----------------------------------------------------
-- Schema jobmatch
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `jobmatch` ;

-- -----------------------------------------------------
-- Schema jobmatch
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `jobmatch` DEFAULT CHARACTER SET latin1 ;
SHOW WARNINGS;
USE `jobmatch` ;

-- -----------------------------------------------------
-- Table `admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `admin` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `admin` (
  `AdminID` INT(11) NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`AdminID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;
CREATE UNIQUE INDEX `Username` ON `admin` (`Username` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `company` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `company` (
  `CompanyID` INT(11) NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(255) NULL DEFAULT NULL,
  `CompanyName` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  `Description` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `PictureURL` VARCHAR(255) NULL DEFAULT NULL,
  `Contact` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`CompanyID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;
CREATE UNIQUE INDEX `Username` ON `company` (`Username` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `companyad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `companyad` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `companyad` (
  `CompanyAdID` INT(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` INT(11) NULL DEFAULT NULL,
  `SalaryRange` VARCHAR(255) NULL DEFAULT NULL,
  `MotivationDescription` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `Status` ENUM('Active', 'Archived') NOT NULL DEFAULT 'Active',
  `CompanyAdRequirement` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`CompanyAdID`),
  CONSTRAINT `companyad_ibfk_1`
    FOREIGN KEY (`ProfessionalID`)
    REFERENCES `professional` (`ProfessionalID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;
CREATE INDEX `idx_status_on_companyad` ON `companyad` (`Status` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `idx_location_on_companyad` ON `companyad` (`Location` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `companyadskill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `companyadskill` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `companyadskill` (
  `CompanyAdID` INT(11) NULL DEFAULT NULL,
  `SkillID` INT(11) NULL DEFAULT NULL,
  `Level` VARCHAR(255) NULL DEFAULT NULL,
  CONSTRAINT `companyadskill_ibfk_1`
    FOREIGN KEY (`CompanyAdID`)
    REFERENCES `companyad` (`CompanyAdID`),
  CONSTRAINT `companyadskill_ibfk_2`
    FOREIGN KEY (`SkillID`)
    REFERENCES `skill` (`SkillID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `jobad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jobad` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `jobad` (
  `JobAdID` INT(11) NOT NULL AUTO_INCREMENT,
  `CompanyID` INT(11) NULL DEFAULT NULL,
  `SalaryRange` VARCHAR(255) NULL DEFAULT NULL,
  `JobDescription` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `Status` ENUM('Active', 'Archived') NOT NULL DEFAULT 'Active',
  `JobRequirement` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`JobAdID`),
  CONSTRAINT `jobad_ibfk_1`
    FOREIGN KEY (`CompanyID`)
    REFERENCES `company` (`CompanyID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;
CREATE INDEX `idx_status_on_jobad` ON `jobad` (`Status` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `idx_location_on_jobad` ON `jobad` (`Location` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `jobadinteraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jobadinteraction` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `jobadinteraction` (
  `InteractionID` INT(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` INT(11) NULL DEFAULT NULL,
  `JobAdID` INT(11) NULL DEFAULT NULL,
  `InteractionType` VARCHAR(255) NULL DEFAULT NULL,
  `InteractionTimestamp` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`InteractionID`),
  CONSTRAINT `jobadinteraction_ibfk_1`
    FOREIGN KEY (`ProfessionalID`)
    REFERENCES `professional` (`ProfessionalID`),
  CONSTRAINT `jobadinteraction_ibfk_2`
    FOREIGN KEY (`JobAdID`)
    REFERENCES `jobad` (`JobAdID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `jobadskill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jobadskill` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `jobadskill` (
  `JobAdID` INT(11) NULL DEFAULT NULL,
  `SkillID` INT(11) NULL DEFAULT NULL,
  `Level` VARCHAR(255) NULL DEFAULT NULL,
  CONSTRAINT `jobadskill_ibfk_1`
    FOREIGN KEY (`JobAdID`)
    REFERENCES `jobad` (`JobAdID`),
  CONSTRAINT `jobadskill_ibfk_2`
    FOREIGN KEY (`SkillID`)
    REFERENCES `skill` (`SkillID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `matchrequests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matchrequests` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `matchrequests` (
  `RequestID` INT(11) NOT NULL AUTO_INCREMENT,
  `CompanyAdID` INT(11) NULL DEFAULT NULL,
  `JobAdID` INT(11) NULL DEFAULT NULL,
  `IsVisibleToCompany` TINYINT(1) NULL DEFAULT NULL,
  `IsVisibleToProfessional` TINYINT(1) NULL DEFAULT NULL,
  `MatchStatus` ENUM('Pending', 'Accepted', 'Rejected') NOT NULL DEFAULT 'Pending',
  PRIMARY KEY (`RequestID`),
  CONSTRAINT `matchrequests_ibfk_1`
    FOREIGN KEY (`CompanyAdID`)
    REFERENCES `companyad` (`CompanyAdID`),
  CONSTRAINT `matchrequests_ibfk_2`
    FOREIGN KEY (`JobAdID`)
    REFERENCES `jobad` (`JobAdID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;
CREATE INDEX `idx_matchstatus_on_matchrequests` ON `matchrequests` (`MatchStatus` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `notification`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notification` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `notification` (
  `NotificationID` INT(11) NOT NULL AUTO_INCREMENT,
  `RecipientID` INT(11) NULL DEFAULT NULL,
  `RecipientType` ENUM('Professional', 'Company') NULL DEFAULT NULL,
  `RequestID` INT(11) NULL DEFAULT NULL,
  `Message` TEXT NULL DEFAULT NULL,
  `IsRead` TINYINT(1) NULL DEFAULT 0,
  `CreatedAt` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`NotificationID`),
  CONSTRAINT `notification_ibfk_1`
    FOREIGN KEY (`RequestID`)
    REFERENCES `matchrequests` (`RequestID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;
CREATE INDEX `idx_professional_on_notification` ON `notification` (`RecipientID` ASC, `RecipientType` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `idx_isread_on_notification` ON `notification` (`IsRead` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `professional`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `professional` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `professional` (
  `ProfessionalID` INT(11) NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(255) NULL DEFAULT NULL,
  `FirstName` VARCHAR(255) NULL DEFAULT NULL,
  `LastName` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  `BriefSummary` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `Status` ENUM('Active', 'Busy') NOT NULL DEFAULT 'Active',
  `PhotoURL` VARCHAR(255) NULL DEFAULT NULL,
  `CVURL` VARCHAR(255) NULL DEFAULT NULL,
  `Contact` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`ProfessionalID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `skill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `skill` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `skill` (
  `SkillID` INT(11) NOT NULL AUTO_INCREMENT,
  `Description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`SkillID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
