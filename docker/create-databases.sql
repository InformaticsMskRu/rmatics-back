-- utf8 everywhere: the tests insert Cyrillic text. Production has a mix (e.g. pynformatics.workshop is utf8,
-- most other pynformatics tables are latin1), so this is a test convenience, not a copy of production.
CREATE DATABASE ejudge CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE DATABASE moodle CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE DATABASE pynformatics CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE DATABASE informatics CHARACTER SET utf8 COLLATE utf8_general_ci;
