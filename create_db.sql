-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema jobmatch
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `jobmatch` ;

-- -----------------------------------------------------
-- Schema jobmatch
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `jobmatch` DEFAULT CHARACTER SET latin1 ;
USE `jobmatch` ;

-- -----------------------------------------------------
-- Table `admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `admin` ;

CREATE TABLE IF NOT EXISTS `admin` (
  `AdminID` INT(11) NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`AdminID`),
  UNIQUE INDEX `Username` (`Username` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `auditlog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `auditlog` ;

CREATE TABLE IF NOT EXISTS `auditlog` (
  `LogID` INT(11) NOT NULL AUTO_INCREMENT,
  `UserID` INT(11) NOT NULL,
  `ActionType` VARCHAR(255) NOT NULL,
  `Details` TEXT NULL DEFAULT NULL,
  `Timestamp` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`LogID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `company` ;

CREATE TABLE IF NOT EXISTS `company` (
  `CompanyID` INT(11) NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(255) NULL DEFAULT NULL,
  `CompanyName` VARCHAR(255) NULL DEFAULT NULL,
  `Password` VARCHAR(255) NULL DEFAULT NULL,
  `Description` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `PictureURL` VARCHAR(255) NULL DEFAULT NULL,
  `Contact` VARCHAR(255) NULL DEFAULT NULL,
  `Email` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`CompanyID`),
  UNIQUE INDEX `Username` (`Username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `professional`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `professional` ;

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
  `Email` VARCHAR(255) NULL DEFAULT NULL,
  `ProfessionalEmail` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`ProfessionalID`),
  UNIQUE INDEX `UniqueProfessionalEmail` (`ProfessionalEmail` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `companyad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `companyad` ;

CREATE TABLE IF NOT EXISTS `companyad` (
  `CompanyAdID` INT(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` INT(11) NULL DEFAULT NULL,
  `SalaryRange` VARCHAR(255) NULL DEFAULT NULL,
  `MotivationDescription` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `Status` ENUM('Active', 'Archived') NOT NULL DEFAULT 'Active',
  `CompanyAdRequirement` TEXT NULL DEFAULT NULL,
  `CreatedAt` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  `UpdatedAt` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`CompanyAdID`),
  INDEX `ProfessionalID` (`ProfessionalID` ASC) VISIBLE,
  INDEX `idx_status_on_companyad` (`Status` ASC) VISIBLE,
  INDEX `idx_location_on_companyad` (`Location` ASC) VISIBLE,
  CONSTRAINT `companyad_ibfk_1`
    FOREIGN KEY (`ProfessionalID`)
    REFERENCES `professional` (`ProfessionalID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `skill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `skill` ;

CREATE TABLE IF NOT EXISTS `skill` (
  `SkillID` INT(11) NOT NULL AUTO_INCREMENT,
  `Description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`SkillID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `companyadskill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `companyadskill` ;

CREATE TABLE IF NOT EXISTS `companyadskill` (
  `CompanyAdID` INT(11) NULL DEFAULT NULL,
  `SkillID` INT(11) NULL DEFAULT NULL,
  `Level` VARCHAR(255) NULL DEFAULT NULL,
  INDEX `CompanyAdID` (`CompanyAdID` ASC) VISIBLE,
  INDEX `SkillID` (`SkillID` ASC) VISIBLE,
  CONSTRAINT `companyadskill_ibfk_1`
    FOREIGN KEY (`CompanyAdID`)
    REFERENCES `companyad` (`CompanyAdID`),
  CONSTRAINT `companyadskill_ibfk_2`
    FOREIGN KEY (`SkillID`)
    REFERENCES `skill` (`SkillID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `jobad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jobad` ;

CREATE TABLE IF NOT EXISTS `jobad` (
  `JobAdID` INT(11) NOT NULL AUTO_INCREMENT,
  `CompanyID` INT(11) NULL DEFAULT NULL,
  `SalaryRange` VARCHAR(255) NULL DEFAULT NULL,
  `JobDescription` TEXT NULL DEFAULT NULL,
  `Location` VARCHAR(255) NULL DEFAULT NULL,
  `Status` ENUM('Active', 'Archived') NOT NULL DEFAULT 'Active',
  `JobRequirement` TEXT NULL DEFAULT NULL,
  `CreatedAt` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  `UpdatedAt` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`JobAdID`),
  INDEX `CompanyID` (`CompanyID` ASC) VISIBLE,
  INDEX `idx_status_on_jobad` (`Status` ASC) VISIBLE,
  INDEX `idx_location_on_jobad` (`Location` ASC) VISIBLE,
  CONSTRAINT `jobad_ibfk_1`
    FOREIGN KEY (`CompanyID`)
    REFERENCES `company` (`CompanyID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `jobadinteraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jobadinteraction` ;

CREATE TABLE IF NOT EXISTS `jobadinteraction` (
  `InteractionID` INT(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` INT(11) NULL DEFAULT NULL,
  `JobAdID` INT(11) NULL DEFAULT NULL,
  `InteractionType` VARCHAR(255) NULL DEFAULT NULL,
  `InteractionTimestamp` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`InteractionID`),
  INDEX `ProfessionalID` (`ProfessionalID` ASC) VISIBLE,
  INDEX `JobAdID` (`JobAdID` ASC) VISIBLE,
  CONSTRAINT `jobadinteraction_ibfk_1`
    FOREIGN KEY (`ProfessionalID`)
    REFERENCES `professional` (`ProfessionalID`),
  CONSTRAINT `jobadinteraction_ibfk_2`
    FOREIGN KEY (`JobAdID`)
    REFERENCES `jobad` (`JobAdID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `jobadskill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jobadskill` ;

CREATE TABLE IF NOT EXISTS `jobadskill` (
  `JobAdID` INT(11) NULL DEFAULT NULL,
  `SkillID` INT(11) NULL DEFAULT NULL,
  `Level` VARCHAR(255) NULL DEFAULT NULL,
  INDEX `JobAdID` (`JobAdID` ASC) VISIBLE,
  INDEX `SkillID` (`SkillID` ASC) VISIBLE,
  CONSTRAINT `jobadskill_ibfk_1`
    FOREIGN KEY (`JobAdID`)
    REFERENCES `jobad` (`JobAdID`),
  CONSTRAINT `jobadskill_ibfk_2`
    FOREIGN KEY (`SkillID`)
    REFERENCES `skill` (`SkillID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `matchrequests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matchrequests` ;

CREATE TABLE IF NOT EXISTS `matchrequests` (
  `RequestID` INT(11) NOT NULL AUTO_INCREMENT,
  `CompanyAdID` INT(11) NULL DEFAULT NULL,
  `JobAdID` INT(11) NULL DEFAULT NULL,
  `IsVisibleToCompany` TINYINT(1) NULL DEFAULT NULL,
  `IsVisibleToProfessional` TINYINT(1) NULL DEFAULT NULL,
  `MatchStatus` ENUM('Pending', 'Accepted', 'Rejected') NOT NULL DEFAULT 'Pending',
  `MatchedAt` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`RequestID`),
  INDEX `CompanyAdID` (`CompanyAdID` ASC) VISIBLE,
  INDEX `JobAdID` (`JobAdID` ASC) VISIBLE,
  INDEX `idx_matchstatus_on_matchrequests` (`MatchStatus` ASC) VISIBLE,
  CONSTRAINT `matchrequests_ibfk_1`
    FOREIGN KEY (`CompanyAdID`)
    REFERENCES `companyad` (`CompanyAdID`),
  CONSTRAINT `matchrequests_ibfk_2`
    FOREIGN KEY (`JobAdID`)
    REFERENCES `jobad` (`JobAdID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `notification`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notification` ;

CREATE TABLE IF NOT EXISTS `notification` (
  `NotificationID` INT(11) NOT NULL AUTO_INCREMENT,
  `RecipientID` INT(11) NULL DEFAULT NULL,
  `RecipientType` ENUM('Professional', 'Company') NULL DEFAULT NULL,
  `RequestID` INT(11) NULL DEFAULT NULL,
  `Message` TEXT NULL DEFAULT NULL,
  `IsRead` TINYINT(1) NULL DEFAULT 0,
  `CreatedAt` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`NotificationID`),
  INDEX `RequestID` (`RequestID` ASC) VISIBLE,
  INDEX `idx_professional_on_notification` (`RecipientID` ASC, `RecipientType` ASC) VISIBLE,
  INDEX `idx_isread_on_notification` (`IsRead` ASC) VISIBLE,
  CONSTRAINT `notification_ibfk_1`
    FOREIGN KEY (`RequestID`)
    REFERENCES `matchrequests` (`RequestID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
