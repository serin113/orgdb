-- Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

-- Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
-- Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

-- Code History:
-- 2019/02/06 - Initial working code and documentation


-- MySQL Script generated by MySQL Workbench
-- Tue Jan 29 20:39:42 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`AffiliationRecordsTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`AffiliationRecordsTable` ;

CREATE TABLE IF NOT EXISTS `mydb`.`AffiliationRecordsTable` (
  `clubID` VARCHAR(50) NOT NULL,    -- record-unique id
  `dateUpdated` DATE NOT NULL,      -- record last modification date
  `region` VARCHAR(10) NULL,        -- school's regional PSGC: 1 to 17
                                    -- https://psa.gov.ph/classification/psgc/downloads/SUMWEBPROV-DEC2018-CODED-HUC-FINAL.pdf
  `level` TINYINT(1) NULL,          -- 1: elementary
                                    -- 2: high school
                                    -- 3: elementary + high school
                                    -- 4: college
  `type` TINYINT(1) NULL,           -- 1: public, 2: private
  `school` VARCHAR(100) NULL,       -- name of school
  `clubName` VARCHAR(100) NULL,     -- name of club
  `address` VARCHAR(200) NULL,      -- school's address
  `city` VARCHAR(45) NULL,          -- school's city
  `province` VARCHAR(45) NULL,      -- school's province
  `adviserName` VARCHAR(100) NULL,  -- club adviser/s' name
  `contact` VARCHAR(45) NULL,       -- club contact no.
  `email` VARCHAR(45) NULL,         -- club email
  PRIMARY KEY (`clubID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`AffiliationTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`AffiliationTable` ;

CREATE TABLE IF NOT EXISTS `mydb`.`AffiliationTable` (
  `affiliationID` VARCHAR(50) NOT NULL,    -- affiliation-unique id
  `affiliated` TINYINT(1) NOT NULL,         -- is club affiliated? 0:no, 1:yes
  `status` VARCHAR(45) NULL,                -- "newly affiliated", "renewing", etc.
  `hasAffiliationForms` TINYINT(1) NULL,    -- are forms submitted? 0:no, 1:yes
  `benefits` VARCHAR(200) NULL,             -- any discounts/sponsorships/scholarships/etc.
  `remarks` VARCHAR(200) NULL,              -- extra remarks
  `schoolYear` YEAR(4) NULL,                -- if s.y. 2018-2019, store 2019
  `yearsAffiliated` INT NULL,               -- duration of affiliation
  `SCA` SMALLINT(10) NULL,                  -- # of club advisers
  `SCM` SMALLINT(10) NULL,                  -- # of club members
  `paymentMode` VARCHAR(200) NULL,          -- means of payment (deposit/check/etc.)
  `paymentDate` DATE NULL,                  -- date paid
  `paymentID` VARCHAR(200) NULL,            -- identifier for payment
  `paymentAmount` INT NULL,                 -- amount paid
  `receiptNumber` VARCHAR(200) NULL,        -- payment receipt number
  `paymentSendMode` VARCHAR(200) NULL,      -- means of sending payment (delivery/in-person/etc.)
  `AffiliationRecordsTable_clubID` VARCHAR(50) NOT NULL,    -- affiliation under which club?
  PRIMARY KEY (`affiliationID`, `AffiliationRecordsTable_clubID`),
  INDEX `fk_AffiliationTable_AffiliationRecordsTable_idx` (`AffiliationRecordsTable_clubID` ASC),
  CONSTRAINT `fk_AffiliationTable_AffiliationRecordsTable`
    FOREIGN KEY (`AffiliationRecordsTable_clubID`)
    REFERENCES `mydb`.`AffiliationRecordsTable` (`clubID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
