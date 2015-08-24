# -*- coding: utf-8 -*-

import os
from collections import defaultdict
import nltk
from nltk.tokenize import RegexpTokenizer


def getpositiveworddictionary ():

    frequency = defaultdict(int)

    with open(os.path.expanduser('~/Downloads/positive-words.txt'), 'r') as f:
        for line in f:
            if line.startswith(';') == False:
                l = line.strip()
                frequency[l] = l

    return frequency

def filterpositives (seq):
    for tuple in seq:
        if len(tuple[1]) > 1 or "!" in tuple[0]: yield (tuple[0] + str(tuple[1]) + "\n")

posdict = getpositiveworddictionary()

#text = "\n    After finishing the Busabout Balkan Trek, I went straight onto the 1 week Busabout Croatia Sail from Split to Dubrovnik. It was an excellent fun filled relaxing week sailing to some of the beautiful islands in the Adriatic sea. There were 22 of us plus our amazing guide and we all got along very well which added to the enjoyment of the week. \n\nIn the first day we set sail from Split at lunchtime and sailed along the coast until we made it to Omis. Here we had our first swim, which was very much needed as it was so hot and humid, in a little bay just outside of Omis. We then docked in Omis and a small group of us climbed up to the top of the Pirate Fortres. It was a more of a hike than walk up steep, uneven ground in very hot weather. The view from the top definitely made it worth while providing a fantastic outlook over the sea and Omis. That night we had the Croatian BBQ dinner which was very lovely.  \n\n The next day we set sail in the morning and then around mid morning stopped for a swim at Pucisca. A bit after lunch we arrived at Makarska. After a little wander around town, a couple of us went back to the boat for a rest, then after our rest we headed off to the beach for a swim before a little walk then made our way back to the boat to get ready for the evenings activities. The evening began with dinner and watching the sunset over the bay, followed by happy hour on the boat before heading out to a bar called Smiles then after that to a nightclub that has been built in a cave. It was a fun evening although the cave was incredibly hot due to all the people, dancing and overall hot weather. \n\n \nFrom Makarska we headed to Hvar, Stari Grad. Of course on our way to Stari Grad we had a lovely refeshing swim stop off the island of Brac. Once in Stari Grad we had some free time for the afternoon, in which another afternoon nap was in order. Later in the evening we caught a bus to a lovely vineyard for some wine tasting and dinner. The setting was absolutely beautiful with vineyards, a little wooden restaurant, some farm animals and a setting sun to top it off. The wines were very lovely and as was the dinner.\n\n \nNext day we stayed on the island of Hvar at Stari Grad for the night but during the day went for a swim stop in a bay of the coast of Hvar. In the afternoon we caught the us around to the main town where we had some free time to explore the town. A few of us climbed up to the Grand Hvar, another fortress. Again this gave amazing views over Hvar, the sea and even to some nearby islands. After this we had a wander around some markets before meeting up with everyone for dinner. After dinner we went to Kiva bar where we had Tequila Booms, cocktails, sang and danced til it was time to leave for the boat.\n\n \nThe next island we stopped off at was Korcula, the home of Marco Polo. After a swim stop we went on land and had a walk through the town. Here we climbed to the top of the bell tower for magnificent views, went to the top of Marco Polos house and then met for dinner. After dinner we made our way back to the boat for happy hour before heading out for the night to a club which sells bucket cockails followed by the Boogie Jungle, a bar/club sort of in a jungle. \n\n \nThe final island we went to was Mijet. This island is a national park where we had free time to explore the national park. A few of us hired kayaks and went for a paddle around the national park for an hour. This was then followed by relaxing in the water and getting an ice cream to eat. Its a beautiful national park and island. This night we had our pirate party so we spent some time getting our pirate costumes ready before having our captains dinner. \n\nWe left early in the morning from Mijet to head for our final destination, Dubrovnik. The week went so fast and it was sad for it to be ending. We arrived in Dubrovnik after lunch and after some orientation to the old town, had some free time to explore. A couple of us caught the cable car which provided a wonderful view of the old town and surroundings. In the evening we went out for a final dinner (one of a few final dinners), before heading to another bucket place and finally dancing the night away in a fortress turned nightclub.\n\n \nThe tour finished after breakfast the next morning which was sad, however about half of us were staying in Dubrovnik for a bit longer so we were able to slowly say our goodbyes. It was a fantastic week getting to see some beautiful places and making some amazing friends, minus the sickness that took over the boat. \n\n\n  "
#text = "\n    Our current and probably final Croatian camp is under a huge Kiwifruit vine in Camp Adriatic II, giving us much needed shade from the sun. Kiwis under the kiwifruit you could say.  We have had a nice holiday here travelling north to south, mostly along the beautiful coastline.  It has been very warm, no or little rain and lots of swimming.  Stephen have acquired quite a tan and Gayle is working on this quietly.\n\nWe were determined to have a summer holiday as we missed out last year, we were too late getting on the road in 2014 hence the Adriatic coast 2015.  We did enjoy several days inland Croatia at Plitvice Lakes National Park but have chosen to spend most of our time on the coast.  Croatia has a coastline of 1700km and some 1250 islands.  Croatia and Turkey are our key destinations and we will experience them in the hottest months of July and August so water is most important.\n\nWe have found Croatian people lovely.  No surprise really as we have grown up and worked with their descendants in NZ.    Dalmatians came to NZ and became successful Kauri gum diggers in Northland as I recall.  They also brought with them wine making skills amongst other things.  We have met many relatives of NZ Croatians who are very proud of their relatives' achievements in NZ. \n\nThe area that made up these now separate countries (the former Yugoslavia) has had a troubled history.  On the gate way between east and west, pivoted between Christian and Islam religion and other beliefs, languages, wealth and poverty, hot and cold climates and so forth, it is no surprise that it has been occupied by its neighbours to north (Austria), West (Italy/ Venice and France) and East (Turkey).  Then of course in 1991 the uprising against Dubrovnik and the rest of Croatia by the Yugoslav People’s Army (YPA), The Homeland War.  Just yesterday I read in the media that a General from the YPA has finally been found and arrested for war crimes. \n\nCroatia’s determination to be independent has been realised and the country is now (after 2012 vote) aligned with the European Union (EU) but keeping its own currency, the Kuna.  It will keep the Kuna until at least 2017.  The years of foreign rule and internal strife have left seemingly few physical scares in the cities.  The old cities are magnificent and it seems that Croatians are getting on with life, probably as they always have.  Economic prosperity has eluded them for a long time.  We observe that people enjoy life and are very welcoming people.  \n \nCroatia has a population similar to NZ at 4.5m, most of whom live on the coast.  We did not get to the capital city Zagreb as a number of fellow travellers advised there were few features worthy of the big drive.  A highlight has been meeting many fellow campers from Slovenia, they all make Slovenia sound so inviting and are all absolutely lovely and friendly. Perhaps a missed opportunity there!  We also have heard nice things about Romania.  We just cannot do it all!\n\nInterestingly there is the little tidal movement along the coast and therefore few waves. (We learnt in Venice the strongest tides are around December, when a lot of the damage is done in the city.)  The water is very warm, I measured 30C in front of our camp.  At a previous camp north of Dubrovnik the water temperature dropped from a nice 26C to 18C after a mildly windy night.  It was so funny watching fellow campers jump into the water only to come up gasping at the unexpected temperature drop!!  I think in NZ we would be delighted to have water at 18C.  We observe few fish (although I am unsure if fish can survive warm temperatures) and the water quality varies, but generally clean.\n\nOur Italian friends said that if we find a nice place, stay there, as much of Croatia is the same.  We would be inclined to agree.  On the road south there have been a couple of places that have been stand outs, those with fewer people and clearer water.\n\nThe Plitvice Lakes were beautiful and a must see.  Given the number of tourists that visit daily they do a great job.  We thought that NZ could learn a little about making the environment a little more accessible as we saw people with disabilities and elderly enjoying the park.  We had arrived just after a heavy rain so everything was at its glorious best for us.\n\nThe offshore islands are of course beautiful and you could spend weeks exploring them all, we just visited a couple finding one of our favourite places on the tip of Peljesac, Lovitse.\n\nWe think fondly of Croatia and it has lived up to our expectations as a fantastic holiday destination.  We feel a little guilty as we have not visited every church or historical site.  We have however seen a lot of the key sites on the Adriatic Coast and feel that we would like to comeback perhaps chartering a boat next time and enjoying the country via the sea.  "
#text = "\n    It is an early start for us today as we have about a 3 hour drive to Plitvice National Park and then another 3 hours to Split. We are on the road by 8.30am and within 30 minutes we have crossed the border into Slovenia...blink and you would miss it! No border crossing, certainly no passport check, nothing. We drive about 40 km and we are at the Croatian border and it is a different story here. We see cars pulled over to the side, luggage out, sniffer dogs and many police. We pull up to the window and show our passports and he asks us \"tourists?\" We reply yes, he stamps our passports and waves us through. We must look so trustworthy...or old I guess. \n\nImmediately upon entering Croatia there is something noticeably different; the roads. They look brand new, no potholes, no patches, just a nice new smooth and WIDE road. We wind our way up through the mountains and about 2 hours later we enter the Plitvice National Park. I had seen it on Getaway about 3 months ago and knew I had to see it in real life. Unfortunately about 5kms out the traffic comes to a standstill. We have no idea why but we have no choice but to sit and wait. \n\nEventually we move a bit and we understand why the traffic has stopped. We have picked the one day of the year they have decided to run the Plitvice marathon and they have closed one of the 2 lanes to traffic. It takes us about an hour to drive the last few kms and park the car but we finally have our entry tickets in hand and begin the walk. \n\nIt is only a few hundred metres before we can hear a waterfall and then we get our first view of the lakes. Spectacular...as good, if not better than the pictures I have seen. The waterfalls are divided into 3 parts; upper, middle and lower. We are looking at the lower but we can see in the distance so much more. We walk approximately a kilometre, catching amazing views along the way and come to the first bus stop. David talks to a young man named Jakob and asks about the difficulty of going further for someone who is using a walking stick and needs an ankle replacement. Because of the marathon the buses are not running as per usual and Jakob says it has disrupted the whole park. He doesn't advise David to go any further as it all becomes quite steep so the decision is made that Scott and I will continue on and David will hang out at the cafe. I'm secretly concerned about getting back to the top myself (it's a long way to the bottom), but I'm determined to see as much as I can. \n\nWe start down the nice wide path through the woodland and all the way along are the most beautiful scenes of the lakes and waterfalls. The sounds are incredible with the chirping of the birds on one side and the crashing of the falls on the other. There don't seem to be that many people and I'm surprised. The colour of the water is a vivid turquoise where it's deep, and crystal clear near the shoreline. We reach the bottom and we are at the middle lake and we can see up to the top lake where there is a boat that ferries people from one side to the other. Not feeling the need to do this we continue down around the lake and we see hundreds of fish trying to swim upstream and then all of a sudden there is a new loud noise in the reeds on the shoreline. Standing, watching and listening we see the source; frogs whose sides puff out every time they croak (sorry Jac but they are fascinating). \n\nWalking along the bottom we come across many more people and, like Cinque Terre, sometimes we have to stop and give way. The path is all made of wooden planks and gets very narrow in places, not to mention a bit slippery. We find ourselves at the top of the bottom waterfall and we cross to the other side. On one side we are being splashed by the waterfall and on the other is the perfect stillness of the lake. The greens in the trees around are as bright as any I've ever seen. It is an absolute feast on the eyes and ears!\n\nThe way around full circle is blocked for some reason so we have to backtrack crossing the lake again and then it's time to start the climb to the top but not before we see some beautiful caves up close and the water looks so tempting to just jump in. There is no swimming in any of the lakes so this is not an option but I'm sure the locals have some secret spots where they take the occasional dip to cool off when it's this hot. \n\nStarting the climb I see a little girl of about 3 walking up the stairs and I say to Scott \"if she can do this then so can I.\" Not that I have any choice. Luckily there are a couple of places to stop and take a breather on the way up and at one of these I see the little girl climbing onto her dads shoulders. She made it about half way to her credit....no easy feat on those little legs. David calls me as I'm climbing but this is no time to talk, so I send him a quick message saying we are nearly back at the top. Of course we make it up but then we still have the walk back to the entrance but after the climb this is a piece of cake. \n\nWe find David at the cafe and of course he has had a wonderful time whilst we've been gone.  He has become an honorary tour guide, greeting buses with Jakob, giving people directions, buying old ladies bottles of water and generally making a nuisance of himself. He has even promised one of our daughters to Jakob if he ever makes it to Australia (he didn't specify which one). \n\nScott and I rehydrate and wolf down a quick hamburger and then it's back to the car to drive to Split. On the way I ask Scott how far we have walked and he tells me just under 8kms! I give myself the proverbial pat on the back...Michelle would be impressed I hope. \n\nWe're hoping the marathon has now finished, but no...we are still held up slightly on the way out (it's now after 3pm). I manage to have a sleep for an hour or so and when I wake up it's like I've been transported to the moon. The landscape has completely changed and it's now craggy cliff faces, rocky surrounds and very stark. Apparently we went through a couple of 5 kilometre long tunnels straight through the mountain and now we are near the coast and we can see the Adriatic. \n\nUnfortunately our host has put an incorrect Google pin on her website and we end up getting lost. We wind up in Castella which is 20 kilometres from where we are supposed to be. I reprogramme  the phone by typing in the address (you wouldn't believe it if I typed it for you) and we drive into the city of Split, around the bay, through the tunnel and we arrive. Luckily Anamarija lives next door so I ring her and she comes down to meet us. \n\nIt had said on her website the apartment was on the second floor but she neglected to mention the 2 flights of stairs up from the garage to get to the ground floor and then the 2 flights up to the apartment. However when we get up there it is worth the climb. The apartment is lovely; very modern and luxurious and with a great view over the Adriatic to the islands. She calls her husband Josip to come and help us with the luggage, gives us a heap of information about where we are and leaves us to settle in. By this time it is after 9pm and we are all exhausted from a huge day. Somehow David manages to get some food delivered (still not sure how he did that), we eat up and then it's off to sleep with the images and sounds of Plitvice in my head.\n\nTomorrow will be a rest day with maybe a trip down to the beach in between naps. I think I've earned it!  "
#text = "\n    By Grant\n\nToday we decided to do a tour of the Palace. We went to the town square and we were greeted by a gorgeous young Croatian woman who spoke beautiful english and would help us with the tour. She gave the kids lollies and after we paid we discovered our real tour guide who was an older lady who was difficult to understand and spoke in a robotic unenthusiastic manner without anyway of engaging the children.  So we fell for the honeypot trap!\n\nIn saying that the Diocletian's Palace is an amazing as it is a living monument where 2000 people still live and run business's today.  The Palace was constructed under the retired Roman emperor Diocletian who built it as a magnificent retirement palace. Some of the ancient ruins included underground basement tunnels which they used for waste disposal which was only discovered in 1958. These tunnels are the most well preserved parts of the palace. They had a Mausoleum, a wonderful square which was a amphitheater.  He was very cruel to the christians. On his travels he bought back Egyptian Sphinxes as souvineers to adorn the Palace.\n\nWhen the nearby Salona was later destroyed by the Slavs and Avars the locals fled to the Palace and made it their home.  From there began lots of changes over many centuries from Gothic through Renaissance, 400 years of Venetian rule with some Baroque architecture. What I found the most interesting was the Venetian influence with its maze of little streets and laneways.  It very much felt like parts of Venice. \n\nAs you all know I love my shopping! Ha Ha! It had lots of small interesting shops with emerging up market boutiques and much to my horror a very modern glass shop front Zara opposite a historic fountain.  Perhaps this demonstrates that it continues to evolve through time. There are also many bars that are open all night long for the young revelers. This woke me up at 4 am and then the church bells rang at 6am. It was certainly a lot quieter in Paris.\n\nPrior to the trip the bits I had read and researched did not convey the beauty of the old town  which is really worth seeing and spending a couple of days to explore.  This contrasts with some of my  other experiences where I have gone  with big expectations and have been mildly disappointed.\n\nTino from our hotel drove us to Marina 40 mins north of Split to pick up our yacht.  Tino was a really nice young guy who went out of his way to explain the history of Split and point out ancient ruins such as the Aqua duct along the way.  He was very engaging with the boys and took a particular liking to Cameron.  Tino is a lawyer but interestingly the Court system grinds to a halt in the summer months as the Judges enjoy their vacation.   So he works in tourism during this time.\n\nWe picked up the boat late in the day.  We motored the boat for an hour to a protected bay in a nearby village.     the boys and i went for a swim and we were shocked to look over to the next adjoining boat to see a young tidy german woman skinny dipping and then drying herself in full display in front of the boys. i would be looking the other way to teach the boys not to look but unfortunately curiosity completely overwhelmed them.  \n\nThe next interesting thing was on anchoring a motor boat arrived and passed over a book to us which was a menu for the local waterfront restaurant so we made a booking and he came back and collected us in an hour.  We enjoyed a wonderful seafood meal in a very non touristy village called Vinišće.\n\nCamerons Fun fact about the Diocletian's Palace.  The palace is built from the same stone as parts of the White House in WASHINGTON.  This could be a legend though!\n\nSplit and collecting our yacht from Sunsail by Cameron\n\nI got up at the sound of the church bells.  We packed our things and made sure we were ready for the boat.  Next we went out into the palace.  We then got on a tour with a girl called Tina.  She was really nice, spoke good English and gave us lollies.  She even got my dad a glass of water because he was thirsty.  Suddenly it all changed and turned into what my dad likes to call the honey pot.  Tina then led us to our actual tour guide.  This lady wasn't enthusiastic at all, spoke too quickly to understand and just wanted to get the job over and done with.  \n\nLater I bought a honey pot with a little bear on top.  We then hopped in a taxi and drove to sunsail.  The taxi driver was awesome I learned more about the Palace then I did with the tour guide.  We finally go to sunsail.  Our skipper Robert and our boat ADAMUS.  Hamish and I had to share a room which was fun because I knew I had company.  We then got out of the harbpur and found a good place to dock for the night.  Later we went swimming for a bit and went to bed.  I forgot to mention that a waiter came out in a rubber ducky with the menu form his restaurant.  We had dinner there and I got a drink called Cockta.  It is a soft drink that you can only get in Croatia. \n\nI \n\n\n \n\n   "
#text = "This was somewhere I had wanted to go ever since I saw the leaflets advertising it. Galvani Park is a high ropes adrenaline course. To start of with we got harnessed up, then one of the instructors gave us a quick tutorial. Then we were off to the trees and ropes beyond. The initial course was only 2 metres off the ground and had simple obstacles, such as a short zip lines, log bridges and tightropes. The intermediate course was 6 metres off the ground and had more extreme obstacles. The final course was 10 metres off the ground and was more challenging,and really got your heart pumping. I loved all of it, I couldn't choose a favourite! One of the best was the zip lines that were 113 metres long and one of the zip lines took you back down to the ground so you had to run along as you landed and try to stay on your feet. After we had completed all the obstacles the owner of the park offered to order pizza for us. He had to take orders from all the other customers, and the pizza had to be delivered, so he advised to do a 3G swing and the static zorb before eating pizza. Jasmin and I went on the giant swing first. After being pulled up to the top I had to pull a handle to release the swing. This meant reached behind me to get the handle, but then when the swing released I wasn't holding on with both hands! As we the swing dropped suddenly forwards we felt like we had left our stomachs at the top! We did the swing twice and the second time still jolted me! Then I did the static zorb. This was 3 metal rings that I was strapped inside, like the Di Vinci man. The instructor swung me round and I tumbled head over heels wondering which way was up. This made me super dizzy and I felt slightly sick. Finally the pizza arrived and we had lunch. It was super good pizza. After lunch we returned to the courses and did my favourite obstacles again before tackling the ninja, extreme course. This started with one zip line and a few obstacles later I confronted a huge zip line 20 metres above a valley. The next stretch of the course included a skate board zip line, a unicycle on a tightrope, a tightrope walk and an Indiana Jones rickety bridge. These were the most challenging obstacles I faced in the entire day. The day left me exhausted but I was very proud of myself for completing the final course."
#text = "\nOur first impression of Croatia after we left Montenegro was of more prosperity. It's all relative but a smooth, well-marked highway along the coast was a big contrast to what we had been bumping along In Albania and Montenegro. \n \nBut our first sight of Dubrovnik was, WOW!!!!!!!!! 10000 times wow. Our daughter Pip had said we needed to go there and now we see what she meant. If you've been there you may share our wonder or, you may just wonder what we're on about. We got dropped at the port and made farewells to our new chums in the van. Got a taxi to the Pile (Pee la) Gate of the old town and dragged our suitcases through the crowds into the eye popper. It's a movie set! Stone walls surround the town; stone buildings, narrow alleys, marble pathways, ancient buildings, crowds of people, shops going great guns in the old buildings, cafes, bars, restaurants, musical performances in the streets - all this in a setting that is in pristine condition after centuries of settlement. Forget the ruins of Greece or Rome, superb as they are, these are ancient and in top working order which is what makes it all so special. And the setting, with the high stone cliff mountains to the east and the Adriatic Sea lapping at the feet of the town walls to the west - simply a symphony of scenery (note the alliteration). \n \nRaymond and My from Sweden had flown in the night before so we enjoyed meeting up with them again for a few days. They were going to stay with us until Venice when Gavin and Heather will also leave for home. \n \nOur apartments were very cute. The Old Town Ivory Apartments. They were in the heart of the town and upstairs above a restaurant in a narrow alley set out for many metres with dozens of tables and chairs from competing bars and eateries. The ambience was nothing more than simply a soirée of sensory salivation (note the......). Fortunately the eating and drinking crowds were not like Courtenay Place on a Friday night so we had no trouble sleeping while there. Shutters over the windows no doubt helped shield sound but we didn't see public drunkeness. The crowds were interesting in themselves as ages and budgets ranged from youthful backpacker types, through young and older families to tour parties, older buffers like us and all nations. Very well behaved given the crowds. The setting, we could see, had a lot to do with the behaviour. Why would you want to be a boofhead in such a beautiful place? \n \nI could rave on about Dubrovnik for hours but suffice to say that we spent our time exploring the town. Walking the city walls a big highlight. Diving off the city seawall into the Adriatic a big one too for me. Swimming at the nearest city beach outside the walls with Lyn. Going up in the gondola with Raymond to the top of the massif to the east. But most of all it was simply walking the narrow alleys, gazing at the buildings, watching the people, choosing another great place to eat at and so on, that made it so special. Unfortunately for Heather she picked up a stomach bug so, in the most special place we had been in to this point, she spent a lot of it unwell and confined to the apartment. \n \nOur last dinner in the town (only there for two nights) was noteable, not only for the food but also for Lyn flirting brazenly with the charming Croatian waiter who, sensing a good tip, returned in kind. He had a pony tail so maybe that explained it. \n \nAfter two nights, off to Split in a rental van. Raymond did the driving as he lives in Europe and is used to driving on the wrong side. He did a fine job and, most of the time, the back seaters kept quiet, so all good. Our road took us north up the Croatian coast. Croatia gets good press as THE destination to head for, partly because of the still relatively unspoilt nature of the coast. There are small resorts and beaches populated with touritas but I reckon go there before it becomes overrun with package deal holidays from all round Europe. It's getting a fair few of them already. \n \nTo put it mildly the scenery along the coast is absurdly picturesque. In the end we were suffering from scenery overload it was that good. We stopped a couple of times during the four hour drive. Our lunch stop was at a small place called Gradac where some of us had a swim while waiting for our food - the beach was literally two metres from our table. \n \nFinally we got to Split. But only after the GPS had sent us on the motorway to Zagreb, the capital city. A minor detour luckily because Zagreb is about 500 Kms north of Split. But as they say, \"garbage in, garbage out\" and that might have had something to do with the GPS glitch. \n \nAt first sight Split looks like many a city. The gritty port area, the high rise apartment blocks, the shopping areas but then you wander into the old town and in particular Diocletian's Palace and you see why daughter Pip again, rated this place as one to \"must see\". Trust ya Pip. \n \nSplit is the second largest city in Croatia but only about the size of Wellington. As a backdrop it has towering eruptions of massif-type rock overlooking it (I needed Diane Toole along for some of this stuff) and the Adriatic on the other flank. It's very dramatic. The piece de resistance though, is Diocletian's Palace. It's actually not a palace, as in being a distinct building. It's a collection of beautiful ancient buildings dating back to Roman times inside ancient walls but operating as a living city with  the usual suspects vying for dollars. Reading about it doesn't do it justice. I had read about it but until I saw it, didn't appreciate its grandeur. I won't attempt to describe it. Go see it for yourself or look it up and read about it - then go and see it. A highlight for Lyn and I was rambling through the basements of the Palace. They've been archaeologically rescued from centuries of burial by rubbish and human occupation. Very atmospheric down in the bowels of the ancient city. \n \nOnly one day in Split unfortunately. It's a place we could easily go back to and explore more. that goes for Croatia in general. We had met up with an old school friend of Raymond's the one night we were there for dinner and it was good to chat with David and his partner Nadine now living and working in Amsterdam. They were going camping the next day in the wilds of Croatia but still had no tent. We also enjoyed swimming at a beach very close to the city. Summer in the Balkans is very settled and hot and perfect for those who like beaches and stuff. \n \nWhat  next? The morning after one night in Split we had a day then we were catching an overnight ferry from Split to Ancona in Italy. The ferry was to arrive at 0800 hours and then we were jumping on a fast train from Ancona to Venice. That was to happen overnight on the 26 and 27 of August.\n\n\n"
text = "\n    Off we set again, sailing towards Bisevo for a visit to the Blue Cave.    \nWe arrived around 10, bought our tickets and about 12 of us boarded the small motorised boat with it's talented captain to navigate our way into the cave.   \n\nThis was not as easy as you’d think, as he had to wait for many other boats to come out first….and then it was our turn.    With heads tucked on our laps and bending way down low, we entered the small tunnel and then wala – we were inside!  Oh wow, it was so nice and something I hope to never forget.  \n The natural color of the water was breathtaking, with the light coming in naturally from underneath.   We could see the rocky bridge formation about 6 metres under the water, but it seemed like it was closer to the surface than that.  \nOur captain was funny saying he was like Noah from the arc and we were all the animals.   On occasion the port workers have to dive down to clear out all the sunglasses and cameras that are dropped in.   I was always disappointed that conditions were not favorable to go into the Blue Grotto near Capri in Italy, so I felt like this really made up for it.  \n\nBack onto the boat and we continued on towards Vis, with a swim stop along the way.  David did two jumps from the top of the boat, so I could get some photographic evidence!  Don’t think I will be doing it again though – once was enough! \nWe also had the pleasure of seeing some dolphins swimming along with the boat.  Oh that's always such an awesome sight :)\n\nWe swam for a while, hanging on to the rope and bobbing around chatting to people.   Everyone on board is getting on really well and making an effort to get to know their fellow travellers.   David borrowed a mask and snorkel and then I had a turn….so nice seeing all the little bright colored fish, but overall there wasn’t much to see in that particular spot.   \n\nLunch time, then another quick swim stop and Nanna nap before we continued on to arrive at Vis around 4.   Another gorgeous island and town, very similar to the others.   We began our walk, and chatted to a salesman as we looked at the masks and snorkels and a pair of shorts for David.  We decided against the shorts as they were $70 and didn’t look worth it.   The salesman became quite insistent on putting us down and was rude and aggressive; quickly asking where we were from and implying that we were typical Aussies, only wanting to buy cheap stuff made in China.   I felt like asking him where the mask and snorkel along with a lot of other junky stuff he was selling had been made then?!  I so wanted to give him a mouthful or two but we just left and walked on, leaving him remonstrating in the background.  \n\nWe wandered around the small town for a while but once again it was oh so hot and we sat and enjoyed a drink and rest for a while in a quaint restaurant where the waiter had great delight in telling us that they order a small beer as a 'baby’ beer.   It tickled his fancy telling us, and he was giggling away.\n\nBack to the boat where we frocked up, ready for the captains dinner.  The food and atmosphere was great and the majority were in party mode.  We spent a bit of time during the day chatting to a young couple from Madrid – Alberto and Patrice about bullfighting, Spanish politics, tips on making Sangria etc etc and the conversations continued during dinner.  As usual it’s great to have a break from just being the two of us and we are enjoying the company of others.  \n\nCheeky crewman Joe fired up the music….so loud it was nearly hurting our ears! LOL.  It was great having a few drinks and bopping away to the music....was a fun night with lots of laughs.   The midnight quiet rule was adhered to with the music being turned down, and we climbed into bed.  Many of the others continued on - think there’s going to be a few sore heads tomorrow.   "
sentences = nltk.sent_tokenize(text.lower().decode('utf-8'))
# SPLIT_SENTENCES = re.compile(u"[.!?:]\s+")
# sentences = SPLIT_SENTENCES.split(text)


tokenizer = RegexpTokenizer(r'\w+')
positivesentences = []
for sentence in sentences:
    tokens = tokenizer.tokenize(sentence)
    positives = []
    for token in tokens:
       if posdict.has_key(token):
        positives.append(token)

    if len(positives) > 0:
        positivesentences.append((sentence, positives))


ratio = len(positivesentences) * 1.0 / (len(sentences) * 1.0)
print ratio
if ratio > 0.333:
    print list(filterpositives(positivesentences))
else:
    print [(tuple[0] + ' ' + str (tuple[1]) + '\n')  for tuple in positivesentences]