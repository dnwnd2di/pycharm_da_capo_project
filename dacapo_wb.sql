CREATE TABLE `ClassroomNumber` (
  `RoomNumber` int(11) NOT NULL,
  PRIMARY KEY (`RoomNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `Master` (
  `Number` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Status` varchar(45) NOT NULL,
  `MasterReason` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `Reservation` (
  `Number` int(11) NOT NULL,
  `StudentID` int(11) NOT NULL,
  `Date` date NOT NULL,
  `StartTime` time NOT NULL,
  `EndTime` time NOT NULL,
  `Status` varchar(45) NOT NULL,
  `Object` varchar(45) DEFAULT NULL,
  `MasterReason` varchar(45) DEFAULT NULL,
  `RoomNumber` int(11) NOT NULL,
  PRIMARY KEY (`Number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ReservationLeader` (
  `Number` int(11) NOT NULL,
  `LeaderID` int(11) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`Number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ReservationMember` (
  `Number` int(11) NOT NULL,
  `LeaderNumber` int(11) NOT NULL,
  `MemberID` int(11) NOT NULL,
  `MemberName` varchar(45) NOT NULL,
  PRIMARY KEY (`Number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Students` (
  `StudentID` int(11) NOT NULL,
  `StudentName` varchar(45) NOT NULL,
  PRIMARY KEY (`StudentID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `User` (
  `StudentID` int(11) NOT NULL,
  `UserName` varchar(45) NOT NULL,
  `UserPassword` varchar(45) NOT NULL,
  `UserEmail` varchar(45) NOT NULL,
  PRIMARY KEY (`StudentID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
