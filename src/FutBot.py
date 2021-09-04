''' FutBot Module '''

from src.BannerMaker import BannerMaker
from src.util import metrics, text
from src.util.date import get_actual_datetime
import src.constants as constants # keys, paths, uri, etc

# mixins
from src.mixins.social import FutBotInstagramMixin, FutBotTwitterMixin
from src.mixins.config import ConfigMixin
from src.mixins.sports import SportsMixin

#sleeping time
SLEEP_TIME = 300

class FutBot(
    FutBotTwitterMixin,
    FutBotInstagramMixin,
    SportsMixin,
    ConfigMixin
):
    ''' FutBot class - manage bot behavior '''

    def __init__(self):
        print("\n\n[FutBot] STARTING... - " + str(get_actual_datetime().strftime('%d-%m-%Y %H:%M:%S')))
        super().__init__()
        self.banner_maker = BannerMaker(constants.uri.API_TEAMS)

    def update(self) -> None:
        ''' Handle bot update functions '''

        self.update_config()

        super().update()

        self.futbot_update()

        print("- Update Flag at {}".format(get_actual_datetime().strftime('%d-%m-%Y %H:%M:%S')))

    def futbot_update(self) -> None:

        if self.tours_to_post and self.tw_get_last_tweet_date() < get_actual_datetime().date():
            for tour in self.tours_to_post:
                try:
                    print("[FutBot] Posting tournament matches for " + tour.name)
                    tour.tweet_id = self.tw_tweet_status_lst(text.tour_to_text.full_info_lst(tour))
                except Exception as exception:
                    print("ERROR: futbot_update()-[tournament]- e: ", exception)
            # TOUR METRICS
            metrics.increase_metric(metrics.TWEETED_TOURNAMENTS, sum(1 for x in self.tours_to_post if x.tweet_id))

        if self.matches_to_post:
            for match in self.matches_to_post:
                try:
                    print('\n[FutBot] Posting match -- {} vs {} --'.format(match.team_1.name, match.team_2.name))

                    match_text = text.match_to_text.full_info(match)
                    match_text += self.tw_get_screen_names([match.team_1.account_id, match.team_2.account_id])

                    banners = self.banner_maker.get_banners(match)

                    if self._config.tweet_match and not match.tweet_id:
                        match.tweet_id = self.tw_tweet_status(match_text, banners['horizontal'])
                    if self._config.post_story_match and not match.story_posted:
                        match.story_posted = self.ig_post_story(banners['vertical'])
                except Exception as exception:
                    print("ERROR: futbot_update()-[match]- e: ", exception)
            # MATCH METRICS
            metrics.increase_metric(metrics.TWEETED_MATCHES, sum(1 for x in self.matches_to_post if x.tweet_id))
            metrics.increase_metric(metrics.POSTED_STORIES, sum(1 for x in self.matches_to_post if x.story_posted))
            if self._config.send_match_message:
                sent_messages = self.tw_send_match_messages([x for x in self.matches_to_post if x.tweet_id])
                metrics.increase_metric(metrics.SENT_TWITTER_MESSAGES, sent_messages)

        # CLEAR LISTS
        self.matches_to_post.clear()
        self.tours_to_post.clear()
