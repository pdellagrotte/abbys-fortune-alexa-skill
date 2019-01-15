# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# TODO: The items below this comment need your attention.
# =========================================================================================================================================

growl_1 = "<audio src='soundbank://soundlibrary/animals/amzn_sfx_dog_med_growl_1x_01'/>"
bark_1 = "<audio src='soundbank://soundlibrary/animals/amzn_sfx_dog_med_bark_1x_01'/>"
bark_2 = "<audio src='soundbank://soundlibrary/animals/amzn_sfx_dog_med_bark_1x_02'/>"
bark_3 = "<audio src='soundbank://soundlibrary/animals/amzn_sfx_dog_med_bark_1x_03'/>"

random_dog_sound = random.choice([bark_1, bark_2, bark_3, growl_1])
pause = "<break time='1s'/>"

SKILL_NAME = "Abby's Fortune"
GET_FACT_MESSAGE = "Welcome to Abby's Fortune." + random_dog_sound + random.choice(["Ready for your fortune? Here it is. ", "Ok here is your fortune.", "I have a bone-tastic fortune for you. Ready?"]) + pause
HELP_MESSAGE = "You can ask me for a fortune but I am pretty useless otherwise"
HELP_REPROMPT = "I can only read fortunes"
STOP_MESSAGE = random.choice(["Goodbye!", "See you at Pet Smart", "Catch you later" + bark_1])
FALLBACK_MESSAGE = "Abby's Fortune can't help you with that.  Instead you can hear your fortune. What can I help you with?" + bark_2
FALLBACK_REPROMPT = 'What can I help you with?' + bark_1
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that." + growl_1

# =========================================================================================================================================
# TODO: Replace this data with your own.  You can find translations of this data at http://github.com/alexa/skill-sample-python-fact/lambda/data
# =========================================================================================================================================

data = [
    bark_2,
    growl_1 + "I can see a visit to Pet Smart in your future",
    "A walk outside will bring you much joy",
    "Putting Bagheera up for adoption will prove to be a wise decision",
    "A bone in the hand is better than a deer antler in the bush",
    "A trip in the car will make for a prosperous future",
    "Leave a bag of chips on the floor, walk outside, and count to 10. You will return to a great reward.",
    "A trip to the dog park near Alewife will bring good luck",
    "Good news will come to you at Pet Smart",
    "South Dakota is nice this time of year, but please leave the cat here",
    "It’s time to get moving. Your spirits will lift accordingly" + bark_3
]

data_end = [
    "Ok, now time to go lay down",
    "Ok, I think I hear the mailman, got to go!",
    "Alright, Bagheera is up to no good, let me go check on him",
    "Ok that is it for now, would you mind picking me up a dog toy with that squeeky thing?",
    "Have a nice day and remember to bring home some treats for me",
    "Ok that is all for now. I promise to stop shedding if you thow away the vacuum.",
    "Ok, that's enough for now. Can we please go for a walk?",
    "That's enough, I'm tired, I think I will go lay on my princess bed. See you later!"
]


# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewSpaceFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        random_fact = random.choice(data)
        random_goodbye = random.choice(data_end)
        speech = GET_FACT_MESSAGE + random_fact + pause + random_goodbye

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, random_fact))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()