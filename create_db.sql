-- Table Professional
CREATE TABLE Professional (
  ProfessionalID INT PRIMARY KEY AUTO_INCREMENT,
  Username VARCHAR(255),
  FirstName VARCHAR(255),
  LastName VARCHAR(255),
  Password VARCHAR(255),
  BriefSummary TEXT,
  Location VARCHAR(255),
  Status ENUM('Active', 'Busy') NOT NULL DEFAULT 'Active',
  PhotoURL VARCHAR(255),
  CVURL VARCHAR(255),
  Contact VARCHAR(255)
);

-- Table Company
CREATE TABLE Company (
  CompanyID INT PRIMARY KEY AUTO_INCREMENT,
  Username VARCHAR(255) UNIQUE,
  CompanyName VARCHAR(255),
  Password VARCHAR(255),
  Description TEXT,
  Location VARCHAR(255),
  PictureURL VARCHAR(255),
  Contact VARCHAR(255)
);

-- Table JobAd
CREATE TABLE JobAd (
  JobAdID INT PRIMARY KEY AUTO_INCREMENT,
  CompanyID INT,
  SalaryRange VARCHAR(255),
  JobDescription TEXT,
  Location VARCHAR(255),
  Status ENUM('Active', 'Archived') NOT NULL DEFAULT 'Active',
  FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID)
);

-- Table Requirement
CREATE TABLE Requirement (
  RequirementID INT PRIMARY KEY AUTO_INCREMENT,
  JobAdID INT,
  Description TEXT,
  FOREIGN KEY (JobAdID) REFERENCES JobAd(JobAdID)
);

-- Table CompanyAd
CREATE TABLE CompanyAd (
  CompanyAdID INT PRIMARY KEY AUTO_INCREMENT,
  ProfessionalID INT,
  SalaryRange VARCHAR(255),
  MotivationDescription TEXT,
  Location VARCHAR(255),
  Status VARCHAR(255),
  FOREIGN KEY (ProfessionalID) REFERENCES Professional(ProfessionalID)
);

-- Table CompanyAdRequirement
CREATE TABLE CompanyAdRequirement (
  CompanyAdRequirementID INT PRIMARY KEY AUTO_INCREMENT,
  CompanyAdID INT,
  Description TEXT,
  FOREIGN KEY (CompanyAdID) REFERENCES CompanyAd(CompanyAdID)
);

-- Table Skill
CREATE TABLE Skill (
  SkillID INT PRIMARY KEY AUTO_INCREMENT,
  Description TEXT
);

-- Table CompanyAdSkill
CREATE TABLE CompanyAdSkill (
  CompanyAdID INT,
  SkillID INT,
  FOREIGN KEY (CompanyAdID) REFERENCES CompanyAd(CompanyAdID),
  FOREIGN KEY (SkillID) REFERENCES Skill(SkillID)
);

-- Table JobAdSkill
CREATE TABLE JobAdSkill (
  JobAdID INT,
  SkillID INT,
  FOREIGN KEY (JobAdID) REFERENCES JobAd(JobAdID),
  FOREIGN KEY (SkillID) REFERENCES Skill(SkillID)
);

-- Table JobAdInteraction
CREATE TABLE JobAdInteraction (
  InteractionID INT PRIMARY KEY AUTO_INCREMENT,
  ProfessionalID INT,
  JobAdID INT,
  InteractionType VARCHAR(255),
  InteractionTimestamp TIMESTAMP,
  FOREIGN KEY (ProfessionalID) REFERENCES Professional(ProfessionalID),
  FOREIGN KEY (JobAdID) REFERENCES JobAd(JobAdID)
);

-- Table JobMatches
CREATE TABLE JobMatches (
  MatchID INT PRIMARY KEY AUTO_INCREMENT,
  ProfessionalID INT,
  JobAdID INT,
  IsVisible BOOLEAN,
  FOREIGN KEY (ProfessionalID) REFERENCES Professional(ProfessionalID),
  FOREIGN KEY (JobAdID) REFERENCES JobAd(JobAdID)
);

-- Table MatchRequests
CREATE TABLE MatchRequests (
  RequestID INT PRIMARY KEY AUTO_INCREMENT,
  CompanyAdID INT,
  JobAdID INT,
  IsVisibleToCompany BOOLEAN,
  IsVisibleToProfessional BOOLEAN,
  MatchStatus ENUM('Pending', 'Accepted', 'Rejected') NOT NULL DEFAULT 'Pending',
  FOREIGN KEY (CompanyAdID) REFERENCES CompanyAd(CompanyAdID),
  FOREIGN KEY (JobAdID) REFERENCES JobAd(JobAdID)
);

-- Table Admin
CREATE TABLE Admin (
  AdminID INT PRIMARY KEY AUTO_INCREMENT,
  Username VARCHAR(255) UNIQUE,
  Password VARCHAR(255)
);


CREATE TABLE Notification (
    NotificationID INT PRIMARY KEY AUTO_INCREMENT,
    EntityID INT,  -- Can be either ProfessionalID or CompanyID
    EntityType ENUM('Professional', 'Company'),
    Message TEXT,
    IsRead BOOLEAN DEFAULT FALSE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_entityid_entitytype_on_notification ON Notification (EntityID, EntityType);
CREATE INDEX idx_isread_on_notification ON Notification (IsRead);

DELIMITER //

CREATE TRIGGER AfterMatchAccepted
AFTER UPDATE ON MatchRequests
FOR EACH ROW
BEGIN
  IF NEW.MatchStatus = 'Accepted' THEN
    -- Insert a notification for the professional
    INSERT INTO Notification (EntityID, EntityType, Message)
    SELECT CompanyAd.ProfessionalID, 'Professional', 
           CONCAT('You have been matched with JobAd ID: ', NEW.JobAdID)
    FROM CompanyAd WHERE CompanyAdID = NEW.CompanyAdID;

    -- Insert a notification for the company
    INSERT INTO Notification (EntityID, EntityType, Message)
    SELECT JobAd.CompanyID, 'Company', 
           CONCAT('Your JobAd ID: ', NEW.JobAdID, ' has been matched')
    FROM JobAd WHERE JobAdID = NEW.JobAdID;
  END IF;
END;

DELIMITER ;

