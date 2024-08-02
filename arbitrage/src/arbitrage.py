import logging


logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

# make a class and inherit it and overload functions needed for 3-way vs 2-way


def american_to_decimal(american_odd):
    """
    Convert American odds to decimal odds.

    Parameters:
    american_odd (int): The American odds.

    Returns:
    float: The decimal odds.
    """
    if american_odd > 0:
        decimal_odds = round((american_odd / 100) + 1, 2)
    else:
        decimal_odds = round((-100 / american_odd) + 1, 2)
    return decimal_odds


def american_to_implied(american_odd):
    """
    Convert American odds to implied probability.

    Parameters:
    american_odd (int): The American odds.

    Returns:
    float: The implied probability.
    """
    implied_odds = 1 / american_to_decimal(american_odd)
    return implied_odds


def is_arbitrage(odd_x, odd_y):
    """
    Check if the given odds represent an arbitrage opportunity.

    Parameters:
    odd_x (int): The first set of American odds.
    odd_y (int): The second set of American odds.

    Returns:
    bool: True if there is an arbitrage opportunity, False otherwise.
    """
    arbitrage_pct = american_to_implied(odd_x) + american_to_implied(odd_y)
    valid_arbitrage = arbitrage_pct < 1
    return valid_arbitrage


def unbiased_arbitrage(odd_x, odd_y, investment):
    """
    Calculate wagers for unbiased arbitrage.

    Parameters:
    odd_x (int): The first set of American odds.
    odd_y (int): The second set of American odds.
    investment (float): The total amount to invest.

    Returns:
    tuple: The amounts to wager on odd_x and odd_y respectively, or None if no arbitrage opportunity exists.
    """
    if is_arbitrage(odd_x, odd_y):
        arbitrage_pct = american_to_implied(odd_x) + american_to_implied(odd_y)
        wager_x = (investment * american_to_implied(odd_x)) / arbitrage_pct
        wager_y = (investment * american_to_implied(odd_y)) / arbitrage_pct
        arbitrage_stakes = (round(wager_x, 2), round(wager_y, 2))
        return arbitrage_stakes
    else:
        logging.warning("Not a valid arbitrage")
        return None


def biased_arbitrage(preferred_odd, cover_odd, investment):
    """
    Calculate wagers for biased arbitrage.

    Parameters:
    preferred_odd (int): The preferred set of American odds.
    cover_odd (int): The covering set of American odds.
    investment (float): The total amount to invest.

    Returns:
    tuple: The amounts to wager on preferred_odd and cover_odd respectively, or None if no arbitrage opportunity exists.
    """
    if is_arbitrage(preferred_odd, cover_odd):
        cover_wager = american_to_implied(cover_odd) * investment
        preferred_wager = investment - cover_wager
        arbitrage_stakes = (round(preferred_wager, 2), round(cover_wager, 2))
        return arbitrage_stakes
    else:
        logging.warning("Not a valid arbitrage")
        return None


def return_on_investment(net_return, investment):
    """
    Calculate the Return on Investment (ROI).

    Parameters:
    net_return (float): The net return from the investment.
    investment (float): The initial investment amount.

    Returns:
    float: The ROI as a ratio of net return to investment.
    """
    roi = net_return / investment
    return roi


def net_return(stake, odds):
    """
    Calculate the net return from a stake based on American odds.

    Parameters:
    stake (float): The amount of money staked.
    odds (int): The American odds for the bet.

    Returns:
    float: The net return from the stake.
    """
    net_return_value = stake * american_to_decimal(odds)
    return net_return_value


def biased_prob_threshold(odd_x, odd_y, investment):
    """
    Calculate the probability threshold of choosing biased over unbiased arbitrage strategy based on American odds.

    This function determines whether there is an arbitrage opportunity between the given odds.
    If so, it calculates the unbiased and biased returns on investment (ROI) and computes the
    probabilities of choosing the biased arbitrage strategies for each set of odds.

    Parameters:
    odd_x (int): The first set of American odds.
    odd_y (int): The second set of American odds.
    investment (float): The total amount to invest.

    Returns:
    tuple: A tuple containing the probabilities (as ratios) of choosing the biased arbitrage for
           each set of odds (biased_prob_a, biased_prob_b). If no arbitrage opportunity exists,
           returns None.
    """
    if is_arbitrage(odd_x, odd_y):
        unbiased_stake = unbiased_arbitrage(odd_x, odd_y, investment)[0]
        unbiased_return = net_return(unbiased_stake, odd_x)
        unbiased_roi = return_on_investment(unbiased_return, investment)

        biased_stake_a = biased_arbitrage(odd_x, odd_y, investment)[0]
        biased_return_a = net_return(biased_stake_a, odd_x)
        biased_roi_a = return_on_investment(biased_return_a, investment)

        biased_stake_b = biased_arbitrage(odd_y, odd_x, investment)[0]
        biased_return_b = net_return(biased_stake_b, odd_y)
        biased_roi_b = return_on_investment(biased_return_b, investment)

        biased_prob_a = unbiased_roi / biased_roi_a
        biased_prob_b = unbiased_roi / biased_roi_b

        return biased_prob_a, biased_prob_b
    else:
        logging.warning("Not a valid arbitrage")
        return None


if __name__ == "__main__":
    # arbitrage = unbiased_arbitrage(150, -125, 429)
    # print(arbitrage[0] * american_to_decimal(150), arbitrage[1] * american_to_decimal(-125))
    # arbitrage = biased_arbitrage(150, -125, 429)
    # print(arbitrage[0] * american_to_decimal(150), arbitrage[1] * american_to_decimal(-125))
    print(biased_prob_threshold(150, 225, 500))
