--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.4

-- Started on 2024-11-06 15:08:35

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: admin
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16470)
-- Name: books; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.books (
    isbn numeric(10,0) NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    publisher character varying(100),
    publicationyear integer,
    imagepath character varying(255),
    available boolean DEFAULT true
);


ALTER TABLE public.books OWNER TO admin;

--
-- TOC entry 216 (class 1259 OID 16476)
-- Name: books_bookid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.books_bookid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.books_bookid_seq OWNER TO admin;

--
-- TOC entry 4321 (class 0 OID 0)
-- Dependencies: 216
-- Name: books_bookid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.books_bookid_seq OWNED BY public.books.isbn;


--
-- TOC entry 217 (class 1259 OID 16477)
-- Name: borrowing; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.borrowing (
    borrowid integer NOT NULL,
    memberid integer NOT NULL,
    isbn integer NOT NULL,
    borrowdate date NOT NULL,
    returndate date,
    duedate date NOT NULL
);


ALTER TABLE public.borrowing OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16480)
-- Name: borrowing_borrowid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.borrowing_borrowid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.borrowing_borrowid_seq OWNER TO admin;

--
-- TOC entry 4322 (class 0 OID 0)
-- Dependencies: 218
-- Name: borrowing_borrowid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.borrowing_borrowid_seq OWNED BY public.borrowing.borrowid;


--
-- TOC entry 219 (class 1259 OID 16481)
-- Name: members; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.members (
    memberid integer NOT NULL,
    firstname character varying(100) NOT NULL,
    lastname character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    joindate date DEFAULT CURRENT_DATE,
    profilepicture character varying(100)
);


ALTER TABLE public.members OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 16485)
-- Name: members_memberid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.members_memberid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_memberid_seq OWNER TO admin;

--
-- TOC entry 4323 (class 0 OID 0)
-- Dependencies: 220
-- Name: members_memberid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.members_memberid_seq OWNED BY public.members.memberid;


--
-- TOC entry 4155 (class 2604 OID 16510)
-- Name: borrowing borrowid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing ALTER COLUMN borrowid SET DEFAULT nextval('public.borrowing_borrowid_seq'::regclass);


--
-- TOC entry 4156 (class 2604 OID 16511)
-- Name: members memberid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members ALTER COLUMN memberid SET DEFAULT nextval('public.members_memberid_seq'::regclass);


--
-- TOC entry 4310 (class 0 OID 16470)
-- Dependencies: 215
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.books (isbn, title, author, publisher, publicationyear, imagepath, available) FROM stdin;
415	The Sum of All Fears	Tom Clancy	Berkley Publishing Group	2002	images/book_covers/The_Sum_of_All_Fears.jpg	t
418	One Hundred Years of Solitude	Gabriel Garcia Marquez	Perennial	1998	images/book_covers/One_Hundred_Years_of_Solitude.jpg	t
422	Slow Waltz in Cedar Bend	Robert James Waller	Warner Books	1994	images/book_covers/Slow_Waltz_in_Cedar_Bend.jpg	t
421	Before I Say Good-Bye	Mary Higgins Clark	Pocket	2001	images/book_covers/Before_I_Say_Good-Bye.jpg	t
352	The Catcher in the Rye	J.D. Salinger	Little, Brown	1991	images/book_covers/The_Catcher_in_the_Rye.jpg	f
417	Lady in Green	Barbara Metzger	Signet Book	2002	images/book_covers/Lady_in_Green/Minor_Indiscretions_(Signet_Regency_Romance).jpg	f
195153448	Classical Mythology	Mark P. O. Morford	Oxford University Press	2002	images/book_covers/Classical_Mythology.jpg	t
357	Pretend You Don't See Her	Mary Higgins Clark	Pocket	1998	images/book_covers/Pretend_You_Don't_See_Her.jpg	t
358	Fast Women	Jennifer Crusie	St. Martin's Press	2001	images/book_covers/Fast_Women.jpg	t
359	Female Intelligence	Jane Heller	St. Martin's Press	2001	images/book_covers/Female_Intelligence.jpg	t
364	The Pillars of the Earth	Ken Follett	Signet Book	1996	images/book_covers/The_Pillars_of_the_Earth.jpg	t
391	Blood Oath	David Morrell	St. Martin's Press	1994	images/book_covers/Blood_Oath.jpg	t
392	The Alibi	Sandra Brown	Warner Books	2000	images/book_covers/The_Alibi.jpg	t
393	The Beach House	James Patterson	Warner Books	2003	images/book_covers/The_Beach_House.jpg	t
394	A Kiss Remembered	Sandra Brown	Warner Books	2003	images/book_covers/A_Kiss_Remembered.jpg	t
395	The Short Forever	Stuart Woods	Signet Book	2003	images/book_covers/The_Short_Forever.jpg	t
20	Mindfulness	Ellen J. Langer	Unknown	1989	images/book_covers/mindfulness.jpg	f
426	The Angelic Darkness	Richard Zimler	Arcadia Books	1999	images/book_covers/The_Angelic_Darkness.jpg	t
427	The Soulbane Stratagem	Norman Jetmundsen	John Hunt Publishing, Ltd.	2000	images/book_covers/The_Soulbane_Stratagem.jpg	t
428	Gangster	Lorenzo Carcaterra	Fawcett Books	2002	images/book_covers/Gangster.jpg	t
429	Hush	Anne Frasier	Onyx Books	2002	images/book_covers/Hush.jpg	t
431	Estudios sobre el amor	Jose Ortega Y Gaset	Downtown Book Center	2001	images/book_covers/Estudios_sobre_el_amor.jpg	t
432	Rebecca	Daphne Du Maurier	Avon	1994	images/book_covers/Rebecca.jpg	t
433	Scarlet Letter	Nathaniel Hawthorne	Signet Book	1993	images/book_covers/Scarlet_Letter.jpg	t
435	Diary of a Mad Mom-To-Be	Laura Wolf	Delta	2003	images/book_covers/Diary_of_a_Mad_Mom-To-Be.jpg	t
437	Contact	Susan Grant	Love Spell	2002	images/book_covers/Contact.jpg	t
438	The Brimstone Wedding	Barbara Vine	Penguin Books Ltd	1997	images/book_covers/The_Brimstone_Wedding.jpg	t
441	Puerto Vallarta Squeeze	Robert James Waller	Warner Books	1995	images/book_covers/Puerto_Vallarta_Squeeze.jpg	t
442	Tree Grows In Brooklyn	Betty Smith	Harpercollins Publisher	1988	images/book_covers/Tree_Grows_In_Brooklyn.jpg	t
439	The Catswold Portal	Shirley Rousseau Murphy	Roc Books	1993	images/book_covers/The_Catswold_Portal.jpg	t
21	Do I Stay Christian?	Brian McLaren	Unknown	2022	images/book_covers/do_i_stay_christian.jpg	f
22	Landmarks	Margaret Silf	Unknown	2015	images/book_covers/landmarks.jpg	f
23	The Choice	Edith Eger	Unknown	2017	images/book_covers/the_choice.jpg	f
24	The Origami Handbook	Rick Beech	Unknown	2003	images/book_covers/the_origami_handbook.jpg	f
25	Still Points	Barbara Brown Taylor	Unknown	2009	images/book_covers/still_points.jpg	f
26	Gold Dust	Ruth Burgess	Unknown	2000	images/book_covers/gold_dust.jpg	f
27	A Year with the Catechism	Raymond Friel	Unknown	2018	images/book_covers/a_year_with_the_catechism.jpg	f
28	The Bible in 365 Stories	Mary Batchelor	Unknown	1985	images/book_covers/childrens_bible.jpg	f
407	Angels & Demons	Dan Brown	Pocket Star	2001	images/book_covers/Angels_&amp;_Demons.jpg	t
411	If I Ever Get Back to Georgia, I'm Gonna Nail My Feet to the Ground	LEWIS GRIZZARD	Ballantine Books	1991	images/book_covers/If_I_Ever_Get_Back_to_Georgia,_I'm_Gonna_Nail_My_Feet_to_the_Ground.jpg	t
413	The Girl Who Loved Tom Gordon	Stephen King	Pocket	2000	images/book_covers/The_Girl_Who_Loved_Tom_Gordon.jpg	t
1874166633	Introducing Nietzsche	Laurence Gane	Natl Book Network	1998	images/book_covers/Introducing_Nietzsche_(Foundations_in_Children's_Ministry).jpg	t
387	Tu Nombre Escrito En El Agua 	Irene Gonzalez Frei	Tusquets	2002	images/book_covers/Tu_Nombre_Escrito_En_El_Agua_(La_Sonrisa_Vertical).jpg	t
390	The Touch of Your Shadow, the Whisper of Your Name	Neal Barrett Jr.	Dell	1996	images/book_covers/The_Touch_of_Your_Shadow,_the_Whisper_of_Your_Name_(Babylon_5,_Book_5).jpg	t
420	Coyote Waits	Tony Hillerman	HarperTorch	1992	images/book_covers/Coyote_Waits_(Joe_Leaphorn/Jim_Chee_Novels).jpg	t
430	Whisper of Evil	Kay Hooper	Bantam Books	2002	images/book_covers/Whisper_of_Evil_(Hooper,_Kay._Evil_Trilogy.).jpg	t
436	Locked in Time	LOIS DUNCAN	Laure Leaf	1986	images/book_covers/Locked_in_Time_(Laurel_Leaf_Books).jpg	t
440	Through Wolf's Eyes	Jane Lindskold	Tor Fantasy	2002	images/book_covers/Through_Wolf's_Eyes_(Wolf).jpg	t
130897930	Core Web Programming	Marty Hall	Prentice Hall PTR	2001	images/book_covers/Core_Web_Programming_(2nd_Edition).jpg	t
201309980	The Unified Modeling Language Reference Manual	James Rumbaugh	Addison-Wesley Professional	1998	images/book_covers/The_Unified_Modeling_Language_Reference_Manual_(Addison-Wesley_Object_Technology_Series).jpg	t
29	All Things New	Fiona Lynch	Unknown	2020	images/book_covers/all_things_new.jpg	f
30	When the Time Was Fulfilled	Arnold Bittlinger	Unknown	1998	images/book_covers/when_the_time_was_fulfilled.jpg	f
31	The Audacity to Believe	Sheila Cassidy	Unknown	1977	images/book_covers/audacity_to_believe.jpg	f
32	The Way Home	Mark Boyle	Unknown	2019	images/book_covers/the_way_home.jpg	f
33	Colour Me Beautiful	Carole Jackson	Unknown	1980	images/book_covers/colour_me_beautiful.jpg	f
34	Eat, Pray, Love	Elizabeth Gilbert	Unknown	2006	images/book_covers/eat_pray_love.jpg	f
35	Tuesdays with Morrie	Mitch Albom	Unknown	1997	images/book_covers/tuesdays_with_morrie.jpg	f
36	A Road Less Travelled	M. Scott Peck	Unknown	1978	images/book_covers/a_road_less_travelled.jpg	f
37	The Waterlog	Roger Deakin	Unknown	1999	images/book_covers/waterlog.jpg	f
38	Building a Bridge	James Martin	Unknown	2017	images/book_covers/building_a_bridge.jpg	f
39	How to use English	Harper Collins	Unknown	2011	images/book_covers/english.jpg	f
40	Chasing Harry Winston	Lauren Weisberger	Unknown	2008	images/book_covers/chasing_harry_winston.jpg	f
41	ChatGPT For Dummies	Pam Baker	Unknown	2024	images/book_covers/chatgpt_for_dummies.jpg	t
42	The Christmas Cottage	Sarah Morgan	Unknown	2024	images/book_covers/the_christmas_cottage.jpg	f
43	Small Things Like These	Claire Keegan	Unknown	2022	images/book_covers/small_things_like_these.jpg	f
44	The Two Towers	J. R. R. Tolkien	Unknown	1974	images/book_covers/the_two_towers.jpg	f
3257217323	Schmatz. Oder Die Sackgasse.	Hans Werner Kettenbach	Diogenes Verlag	2003	images/book_covers/Schmatz._Oder_Die_Sackgasse..jpg	t
408	The Deal	Joe Hutsko	Tor Books	2000	images/book_covers/The_Deal.jpg	t
3596156904	Amok.	Emmanuel Carrere	Fischer	2003	images/book_covers/Amok..jpg	t
3442150663	Der Mossad.	Victor Ostrovsky	Goldmann	2000	images/book_covers/Der_Mossad..jpg	t
684857502	TEXASVILLE : A Novel	Larry McMurtry	Simon & Schuster	1999	images/book_covers/TEXASVILLE_:_A_Novel.jpg	t
1869500830	Choose to Be Happy: Your Step-By-Step Guide	Wayne Froggatt	Consortium Book	1998	images/book_covers/Choose_to_Be_Happy:_Your_Step-By-Step_Guide.jpg	t
1845170423	Cocktail Classics	David Biggs	Connaught	2004	images/book_covers/Cocktail_Classics.jpg	t
60093269	Two of a Kind #30: Making a Splash	Mary-Kate & Ashley Olsen	HarperEntertainment	2003	images/book_covers/Two_of_a_Kind_#30:_Making_a_Splash_(Two_of_a_Kind,_30).jpg	t
525447644	From One to One Hundred	Teri Sloat	Dutton Books	1991	images/book_covers/From_One_to_One_Hundred.jpg	t
231128444	Slow Food	Carlo Petrini	Columbia University Press	2003	images/book_covers/Slow_Food(The_Case_For_Taste).jpg	t
192126040	Republic (World's Classics)	Plato	Oxford University Press	1996	images/book_covers/Republic_(World's_Classics).jpg	t
300043813	Pleasures of the Belle Epoque	Charles Rearick	Yale University Press	1988	images/book_covers/Pleasures_of_the_Belle_Epoque:_Entertainment_and_Festivity_in_Turn-Of-The-Century_France.jpg	t
310250641	Line of Duty	Terri Blackstock	Zondervan Publishing Company	2003	images/book_covers/Line_of_Duty_(Newpointe_911).jpg	t
393025470	Exposure of the Heart	Rebecca Busselle	Norton	1989	images/book_covers/Exposure_of_the_Heart:_A_Photographer's_Year_in_an_Institution.jpg	t
451205618	The Banished Bride	Andrea Pickens	Signet Book	2002	images/book_covers/The_Banished_Bride_(Signet_Regency_Romance).jpg	t
156029952	Timoleon Vieta Come Home : A Sentimental Journey	Dan Rhodes	Harvest Books	2004	images/book_covers/Timoleon_Vieta_Come_Home_:_A_Sentimental_Journey.jpg	t
312979002	Jester Leaps In	Alan Gordon	St. Martin's Minotaur	2002	images/book_covers/Jester_Leaps_In.jpg	t
553816136	A Year of Russian Feasts	Catherine Cheremeteff Jones	Bantam	2003	images/book_covers/A_Year_of_Russian_Feasts.jpg	t
195124995	For Cause and Comrades: Why Men Fought in the Civil War	James M. McPherson	Oxford University Press	1998	images/book_covers/For_Cause_and_Comrades:_Why_Men_Fought_in_the_Civil_War.jpg	t
1853914266	Really Useful: Student Book (Really Useful Series)	Silvana Franco	Murdoch Books UK	1995	images/book_covers/Really_Useful:_Student_Book_(Really_Useful_Series).jpg	t
738702315	Llewellyn's Witchy Day Planner 2004 Calendar	Ellen Dugan	Llewellyn Publications	2003	images/book_covers/Llewellyn's_Witchy_Day_Planner_2004_Calendar.jpg	t
806524103	The Teen Book of Shadows: Star Signs, Spells, Potions, and Powers	Patricia Telesco	Citadel Press	2004	images/book_covers/The_Teen_Book_of_Shadows:_Star_Signs,_Spells,_Potions,_and_Powers.jpg	t
1842552678	The Book of Dead Days (Book of Dead Days S.)	Marcus Sedgwick	Orion Children's	2004	images/book_covers/The_Book_of_Dead_Days_(Book_of_Dead_Days_S.).jpg	t
1857584112	GCSE English (GCSE Textbooks)	Ian Barr	Letts Educational Ltd	1996	images/book_covers/GCSE_English_(GCSE_Textbooks).jpg	t
1857584139	GCSE Mathematics (GCSE Textbooks)	Mary Rouncefield	Letts Educational Ltd	1996	images/book_covers/GCSE_Mathematics_(GCSE_Textbooks).jpg	t
310700450	Girlz Want to Know	Suzie Shellenberger	Zonderkidz	2001	images/book_covers/Girlz_Want_to_Know.jpg	t
743247680	What Smart Girls Know About the SAT: How to Beat the Gender Bias	Cynthia Johnson	Kaplan	2003	images/book_covers/What_Smart_Girls_Know_About_the_SAT:_How_to_Beat_the_Gender_Bias.jpg	t
310232538	Lily's Ultimate Party	Nancy N. Rue	Zonderkidz	2001	images/book_covers/Lily's_Ultimate_Party_(Young_Women_of_Faith:_Lily_Series,_Book_4).jpg	t
310702496	Lights, Action, Lily!	Nancy Rue	Zonderkidz	2002	images/book_covers/Lights,_Action,_Lily!_(Young_Women_of_Faith:_Lily_Series,_Book_7).jpg	t
310702500	Lily Rules!	Nancy Rue	Zonderkidz	2002	images/book_covers/Lily_Rules!_(Young_Women_of_Faith:_Lily_Series,_Book_8).jpg	t
310702607	Rough & Rugged Lily	Nancy N. Rue	Zonderkidz	2002	images/book_covers/Rough_&amp;_Rugged_Lily_(Young_Women_of_Faith:_Lily_Series,_Book_9).jpg	t
310702623	Lily Speaks!	Nancy N. Rue	Zonderkidz	2002	images/book_covers/Lily_Speaks!_(Young_Women_of_Faith:_Lily_Series,_Book_10).jpg	t
1865086460	Studying Part Time Without Stress	Teresa De Fazio	Allen & Unwin	2002	images/book_covers/Studying_Part_Time_Without_Stress.jpg	t
764224808	Cross My Heart (Hidden Diary)	Sandra Byrd	Bethany House Publishers	2001	images/book_covers/Cross_My_Heart_(Hidden_Diary).jpg	t
1400303214	Stranger Online (Todaysgirlsonly, 1)	Terry Brown	Tommy Nelson	2003	images/book_covers/Stranger_Online_(Todaysgirlsonly,_1).jpg	t
1400303222	Portrait Of Lies (Todaysgirlsonly, 2)	Terry K. Brown	Tommy Nelson	2003	images/book_covers/Portrait_Of_Lies_(Todaysgirlsonly,_2).jpg	t
1400303230	Tangled Web (Todaysgirlsonly, 3)	Terry Brown	Tommy Nelson	2003	images/book_covers/Tangled_Web_(Todaysgirlsonly,_3).jpg	t
1400303249	R U 4 Real (Todaysgirlsonly, 4)	Terry Brown	Tommy Nelson	2003	images/book_covers/R_U_4_Real_(Todaysgirlsonly,_4).jpg	t
1414048688	Professor Terwilliger and Tim Neptune I	Cal Patterson	1stBooks Library	2004	images/book_covers/Professor_Terwilliger_and_Tim_Neptune_I.jpg	t
1562477900	Amelia Hits the Road (Amelia)	Marissa Moss	Pleasant Company Publications	1999	images/book_covers/Amelia_Hits_the_Road_(Amelia).jpg	t
1578567475	Hyperlinkz Book 1 : Digital Disaster (Hyperlinkz)	ROBERT ELMER	WaterBrook Press	2004	images/book_covers/Hyperlinkz_Book_1_:_Digital_Disaster_(Hyperlinkz).jpg	t
1584853301	Oh Boy, Amelia (Amelia)	Marissa Moss	Pleasant Company Publications	2001	images/book_covers/Oh_Boy,_Amelia_(Amelia).jpg	t
1584855096	Amelia's School Survival Guide (Amelia)	Marissa Moss	Pleasant Company Publications	2002	images/book_covers/Amelia's_School_Survival_Guide_(Amelia).jpg	t
140375376	Escape from Egypt: A Novel	Sonia Levitin	Puffin Books	1996	images/book_covers/Escape_from_Egypt:_A_Novel.jpg	t
553211994	The Jungle Books and Just So Stories	Kipling Rudyard	Bantam Classics	1986	images/book_covers/The_Jungle_Books_and_Just_So_Stories.jpg	t
679754750	Skinned Alive: Stories	Edmund White	Vintage Books USA	1996	images/book_covers/Skinned_Alive:_Stories.jpg	t
803267177	Wigwam Evenings: Sioux Folk Tales Retold	Charles A. Eastman	University of Nebraska Press	1990	images/book_covers/Wigwam_Evenings:_Sioux_Folk_Tales_Retold.jpg	t
843101083	Off-The-Wall (Mad Libs, No. 6)	Roger Price	Price Stern Sloan	1970	images/book_covers/Off-The-Wall_(Mad_Libs,_No._6).jpg	t
753506440	Death Cults: Murder, Mayhem and Mind Control (True Crime Series)	Jack Sargeant	Virgin Publishing	2002	images/book_covers/Death_Cults:_Murder,_Mayhem_and_Mind_Control_(True_Crime_Series).jpg	t
441011799	Singularity Sky	Charles Stross	Ace	2004	images/book_covers/Singularity_Sky.jpg	t
375415343	A Whistling Woman	A.S. BYATT	Knopf	2002	images/book_covers/A_Whistling_Woman.jpg	t
9813056398	Broken Mirror : True Stories About Drug Abuse	Dawn Tan	Angsana Books	2000	images/book_covers/Broken_Mirror_:_True_Stories_About_Drug_Abuse.jpg	t
70704309	Electronic filter design handbook	Arthur Bernard Williams	McGraw-Hill	1981	images/book_covers/Electronic_filter_design_handbook.jpg	t
321196775	A Brief History of Western Civilization	Mark Kishlansky	Longman	2004	images/book_covers/A_Brief_History_of_Western_Civilization_:_The_Unfinished_Legacy,_Volume_II_(Chapters_14-30)_(4th_Edi.jpg	t
310702631	Horse Crazy Lily	Nancy N. Rue	Zonderkidz	2003	images/book_covers/Horse_Crazy_Lily_(Young_Women_of_Faith:_Lily_Series,_Book_11).jpg	t
310702640	Lily's Church Camp Adventure 	Nancy N. Rue	Zonderkidz	2003	images/book_covers/Lily's_Church_Camp_Adventure_(Young_Women_of_Faith:_Lily_Series,_Book_12).jpg	t
310705550	Lily's Passport to Paris	Nancy N. Rue	Zonderkidz	2003	images/book_covers/Lily's_Passport_to_Paris_(Young_Women_of_Faith).jpg	t
696203650	Better Homes and Gardens Crockery Cookbook	Lisa L. Mannes	Better Homes and Gardens Books	1994	images/book_covers/Better_Homes_and_Gardens_Crockery_Cookbook_(Better_Homes_&amp;_Gardens_(Hardcover)).jpg	t
1584857447	True Stories: Girls' Inspiring Stories of Courage and Heart	Trula Magruder	American Girl	2003	images/book_covers/True_Stories:_Girls'_Inspiring_Stories_of_Courage_and_Heart_(American_Girl_Library_(Middleton,_Wis.).jpg	t
396	Dead Aim	IRIS JOHANSEN	Bantam Books	2004	images/book_covers/Dead_Aim.jpg	f
671015885	Star Trek: First Contact (Star Trek)	J.M. Dillard	Simon & Schuster	1997	images/book_covers/Star_Trek:_First_Contact_(Star_Trek).jpg	t
767409752	A Guided Tour of Rene Descartes\n	Christopher  Biffle	McGraw-Hill	2000	images/book_covers/A_Guided_Tour_of_Rene_Descartes'_Meditations_on_First_Philosophy_with_Complete_Translations_of_the_M.jpg	t
802713904	Tycho & Kepler	Kitty Ferguson	Walker & Company	2002	images/book_covers/Tycho_&amp;_Kepler.jpg	t
1902852036	All the Queen's Men	Nick Elwood	Kiki Press	1999	images/book_covers/All_the_Queen's_Men.jpg	t
3404204433	Am Ende des Regenbogens.	Alan Dean Foster	Labbe	2002	images/book_covers/Am_Ende_des_Regenbogens..jpg	t
3462017942	Die Massenpsychologie des Faschismus.	Wilhelm Reich	Kiepenheuer & Witsch	1986	images/book_covers/Die_Massenpsychologie_des_Faschismus..jpg	t
226751260	The Jack-Roller: A Delinquent Boy's Own Story	Clifford R. Shaw	University of Chicago Press	1966	images/book_covers/The_Jack-Roller:_A_Delinquent_Boy's_Own_Story_(Phoenix_Books).jpg	t
375804072	There Comes a Time	MILTON MELTZER	Random House Books	2001	images/book_covers/There_Comes_a_Time_:_The_Struggle_for_Civil_Rights_(Landmark_Books).jpg	t
395611563	Walking With the Great Apes	Sy Montgomery	Mariner Books	1992	images/book_covers/Walking_With_the_Great_Apes:_Jane_Goodall,_Dian_Fossey,_Birute_Galdikas.jpg	t
\.


--
-- TOC entry 4312 (class 0 OID 16477)
-- Dependencies: 217
-- Data for Name: borrowing; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.borrowing (borrowid, memberid, isbn, borrowdate, returndate, duedate) FROM stdin;
16	1	22	2024-10-13	2024-10-13	2024-11-12
17	1	23	2024-10-13	2024-10-13	2024-11-12
18	1	24	2024-10-13	2024-10-13	2024-11-12
19	1	25	2024-10-14	2024-10-14	2024-11-13
21	1	27	2024-10-14	2024-10-23	2024-11-13
24	1	30	2024-10-23	\N	2024-11-22
25	8	31	2024-10-23	\N	2024-11-22
26	9	32	2024-10-23	\N	2024-11-22
27	8	20	2024-10-23	\N	2024-11-22
20	1	26	2024-08-14	2024-10-30	2024-11-08
37	12	22	2024-10-30	2024-10-30	2024-11-29
33	1	40	2024-10-30	2024-10-30	2024-11-29
36	4	21	2024-10-30	2024-10-30	2024-11-29
34	1	37	2024-10-30	2024-10-30	2024-11-29
35	8	33	2024-10-30	2024-10-30	2024-11-29
39	6	24	2024-10-30	2024-10-30	2024-11-29
38	1	25	2024-10-30	2024-10-30	2024-11-29
31	1	28	2024-10-30	2024-10-30	2024-11-29
40	1	23	2024-10-30	\N	2024-11-29
41	5	26	2024-10-30	\N	2024-11-29
42	4	40	2024-10-30	\N	2024-11-29
30	1	38	2024-10-30	2024-10-30	2024-12-06
43	1	21	2024-10-30	\N	2024-11-29
44	1	33	2024-10-30	\N	2024-11-29
22	5	34	2024-10-16	2024-10-30	2024-11-15
45	5	22	2024-10-30	\N	2024-11-29
29	1	36	2024-10-30	2024-10-30	2024-11-29
32	1	39	2024-10-30	2024-10-30	2024-11-29
46	1	24	2024-10-30	\N	2024-11-29
47	5	37	2024-10-30	\N	2024-11-29
48	4	25	2024-10-30	\N	2024-11-29
49	4	38	2024-10-30	\N	2024-11-29
50	4	28	2024-10-30	\N	2024-11-29
23	1	29	2024-10-23	2024-10-30	2024-11-22
51	5	34	2024-10-30	\N	2024-11-29
52	8	36	2024-10-30	\N	2024-11-29
28	6	35	2024-10-23	2024-10-30	2024-11-22
53	5	35	2024-10-30	\N	2024-11-29
54	14	39	2024-10-30	\N	2024-11-29
55	1	29	2024-10-30	\N	2024-11-29
56	1	27	2024-10-30	\N	2024-11-29
58	1	42	2024-10-31	\N	2024-11-30
59	1	43	2024-10-31	2024-10-31	2024-11-30
60	6	44	2024-10-31	\N	2024-11-30
61	1	43	2024-10-31	\N	2024-11-30
57	1	41	2024-10-31	2024-10-31	2024-11-30
62	1	41	2024-11-03	2024-11-04	2024-12-03
63	4	417	2024-11-05	\N	2024-12-05
64	1	421	2024-11-05	2024-11-05	2024-12-05
65	6	352	2024-11-05	\N	2024-12-05
66	5	396	2024-11-06	\N	2024-12-06
\.


--
-- TOC entry 4314 (class 0 OID 16481)
-- Dependencies: 219
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.members (memberid, firstname, lastname, email, joindate, profilepicture) FROM stdin;
1	Alan	Maizon	alanmaizon@hotmail.com	2024-10-13	images/profile_pics/alan.png
4	Anna 	Phalan	annaphalan@hotmail.com	2024-10-13	images/profile_pics/anna.png
5	Tim 	Phalan	timphalan@hotmail.com	2024-10-14	images/profile_pics/tim.png
6	Sandy	King	sandyking@hotmail.com	2024-10-14	images/profile_pics/sandy.png
10	Sally	Phalan	sallyphalan@hotmail.com	2024-10-14	images/profile_pics/sally.png
12	Amado	Nervio	amadonervio@gmail.com	2024-10-17	images/profile_pics/amado.png
14	Cindy	Lopez	cindylopez@gmail.com	2024-10-30	images/profile_pics/cindy.png
16	Leo	Sempilon	leosampi@gmail.com	2024-10-30	images/profile_pics/leo.png
18	Laura	Parvel	lauraparvel@hotmail.com	2024-10-30	images/profile_pics/laura.png
20	Joe	Miller	joemiller@gmail.com	2024-10-30	images/profile_pics/joe.png
13	Sean	Ceola	seanceol@gmail.com	2024-10-23	images/profile_pics/sean.png
8	Juan	Celli	juancello@hotmail.com	2024-10-14	images/profile_pics/juan.png
9	Azul	Guevara	azulpacto@hotmail.com	2024-10-14	images/profile_pics/azul.png
15	Dorothy	Adehia	doredelhi@gmail.com	2024-10-30	images/profile_pics/dorothy.png
\.


--
-- TOC entry 4324 (class 0 OID 0)
-- Dependencies: 216
-- Name: books_bookid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.books_bookid_seq', 442, true);


--
-- TOC entry 4325 (class 0 OID 0)
-- Dependencies: 218
-- Name: borrowing_borrowid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.borrowing_borrowid_seq', 66, true);


--
-- TOC entry 4326 (class 0 OID 0)
-- Dependencies: 220
-- Name: members_memberid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.members_memberid_seq', 22, true);


--
-- TOC entry 4159 (class 2606 OID 16527)
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (isbn);


--
-- TOC entry 4161 (class 2606 OID 16492)
-- Name: borrowing borrowing_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_pkey PRIMARY KEY (borrowid);


--
-- TOC entry 4163 (class 2606 OID 16494)
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (memberid);


--
-- TOC entry 4164 (class 2606 OID 16533)
-- Name: borrowing borrowing_bookid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_bookid_fkey FOREIGN KEY (isbn) REFERENCES public.books(isbn);


--
-- TOC entry 4165 (class 2606 OID 16528)
-- Name: borrowing borrowing_isbn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_isbn_fkey FOREIGN KEY (isbn) REFERENCES public.books(isbn);


--
-- TOC entry 4166 (class 2606 OID 16500)
-- Name: borrowing borrowing_memberid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_memberid_fkey FOREIGN KEY (memberid) REFERENCES public.members(memberid);


--
-- TOC entry 2048 (class 826 OID 16512)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO admin;


--
-- TOC entry 2049 (class 826 OID 16513)
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO admin;


--
-- TOC entry 2050 (class 826 OID 16514)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO admin;


--
-- TOC entry 2051 (class 826 OID 16515)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO admin;


-- Completed on 2024-11-06 15:08:39

--
-- PostgreSQL database dump complete
--

