CREATE TABLE scenes
(
    name    TEXT    PRIMARY KEY
);

INSERT INTO "scenes" VALUES('The Parrot Sketch');

CREATE TABLE roles
(
    scene   TEXT    NOT NULL,
    name    TEXT    NOT NULL,
    actor   TEXT    NOT NULL,
    UNIQUE(scene, name, actor)
);

INSERT INTO "roles" VALUES('The Parrot Sketch', 'MR PRALINE', 'John Cleese');
INSERT INTO "roles" VALUES('The Parrot Sketch', 'SHOP OWNER', 'Machale Palin');

CREATE TABLE scripts
(
    scene   TEXT    NOT NULL REFERENCES scenes(name),
    seq     INTEGER NOT NULL,
    role    TEXT    REFERENCES roles(name),
    line    TEXT    NOT NULL
);

INSERT INTO "scripts" VALUES('The Parrot Sketch', 1, NULL, 'A customer enters a pet shop.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 1, 'MR PRALINE', '''Ello, I wish to register a complaint.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 2, 'OWNER', '(no response)');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 3, 'MR PRALINE', '''Ello, Miss?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 4, 'OWNER', 'What do you mean "miss"?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 5, 'MR PRALINE', 'I''m sorry, I have a cold. I wish to make a complaint!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 6, 'OWNER', 'We''re closin'' for lunch.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 7, 'MR PRALINE', 'Never mind that, my lad. I wish to complain about this parrot what I purchased not half an hour ago from this very boutique.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 8, 'OWNER', 'Oh yes, the, uh, the Norwegian Blue...What''s,uh...What''s wrong with it?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 9, 'MR PRALINE', 'I''ll tell you what''s wrong with it, my lad. ''E''s dead, that''s what''s wrong with it!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 10, 'OWNER', 'No, no, ''e''s uh,...he''s resting.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 11, 'MR PRALINE', 'Look, matey, I know a dead parrot when I see one, and I''m looking at one right now.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 12, 'OWNER', 'No no he''s not dead, he''s, he''s restin''! Remarkable bird, the Norwegian Blue, idn''it, ay? Beautiful plumage!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 13, 'MR PRALINE', 'The plumage don''t enter into it. It''s stone dead.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 14, 'OWNER', 'Nononono, no, no! ''E''s resting!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 15, 'MR PRALINE', 'All right then, if he''s restin'', I''ll wake him up! (shouting at the cage) ''Ello, Mister Polly Parrot! I''ve got a lovely fresh cuttle fish for you if you show...');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 16, 'OWNER', '(hits the cage) There, he moved!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 17, 'MR PRALINE', 'No, he didn''t, that was you hitting the cage!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 18, 'OWNER', 'I never!!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 19, 'MR PRALINE', 'Yes, you did!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 20, 'OWNER', 'I never, never did anything...');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 21, 'MR PRALINE', '(yelling and hitting the cage repeatedly) ''ELLO POLLY!!!!! Testing! Testing! Testing! Testing! This is your nine o''clock alarm call!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 22, 'MR PRALINE', '(Takes parrot out of the cage and thumps its head on the counter. Throws it up in the air and watches it plummet to the floor.)');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 23, 'MR PRALINE', 'Now that''s what I call a dead parrot.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 24, 'OWNER', 'No, no.....No, ''e''s stunned!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 25, 'MR PRALINE', 'STUNNED?!?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 26, 'OWNER', 'Yeah! You stunned him, just as he was wakin'' up! Norwegian Blues stun easily, major.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 27, 'MR PRALINE', 'Um...now look...now look, mate, I''ve definitely ''ad enough of this. That parrot is definitely deceased, and when I purchased it not ''alf an hour ago, you assured me that its total lack of movement was due to it bein'' tired and shagged out following a prolonged squawk.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 28, 'OWNER', 'Well, he''s...he''s, ah...probably pining for the fjords.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 29, 'MR PRALINE', 'PININ'' for the FJORDS?!?!?!? What kind of talk is that?, look, why did he fall flat on his back the moment I got ''im home?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 30, 'OWNER', 'The Norwegian Blue prefers keepin'' on it''s back! Remarkable bird, id''nit, squire? Lovely plumage!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 31, 'MR PRALINE', 'Look, I took the liberty of examining that parrot when I got it home, and I discovered the only reason that it had been sitting on its perch in the first place was that it had been NAILED there.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 32, 'OWNER', '(pause) Well, o''course it was nailed there! If I hadn''t nailed that bird down, it would have nuzzled up to those bars, bent ''em apart with its beak, and VOOM! Feeweeweewee!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 33, 'MR PRALINE', '"VOOM"?!? Mate, this bird wouldn''t "voom" if you put four million volts through it! ''E''s bleedin'' demised!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 34, 'OWNER', 'No no! ''E''s pining!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 35, 'MR PRALINE', '''E''s not pinin''! ''E''s passed on! This parrot is no more! He has ceased to be! ''E''s expired and gone to meet ''is maker! ''E''s a stiff! Bereft of life, ''e rests in peace! If you hadn''t nailed ''im to the perch ''e''d be pushing up the daisies! ''Is metabolic processes are now ''istory! ''E''s off the twig! ''E''s kicked the bucket, ''e''s shuffled off ''is mortal coil, run down the curtain and joined the bleedin'' choir invisibile!! THIS IS AN EX-PARROT!!');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 36, 'OWNER', '(pause) Well, I''d better replace it, then. (he takes a quick peek behind the counter) Sorry squire, I''ve had a look ''round the back of the shop, and uh, we''re right out of parrots.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 37, 'MR PRALINE', 'I see. I see, I get the picture.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 38, 'OWNER', 'I got a slug.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 39, 'MR PRALINE', '(pause) Pray, does it talk?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 40, 'OWNER', 'Nnnnot really.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 41, 'MR PRALINE', 'WELL IT''S HARDLY A BLOODY REPLACEMENT, IS IT?!!???!!?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 42, 'OWNER', 'N-no, I guess not. (gets ashamed, looks at his feet)');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 43, 'MR PRALINE', 'Well.');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 44, 'OWNER', '(pause, quietly) D''you.... d''you want to come back to my place?');
INSERT INTO "scripts" VALUES('The Parrot Sketch', 45, 'MR PRALINE', '(looks around) Yeah, all right, sure.');
