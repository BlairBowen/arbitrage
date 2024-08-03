import logging

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

class Arbitrage:
    """
    A base class for handling arbitrage calculations with two odd bets.

    Attributes:
    odd_x (int): The first set of American odds.
    odd_y (int): The second set of American odds.
    investment (float): The total amount to invest.
    """

    def __init__(self, odd_x, odd_y, investment):
        self.odd_x = odd_x
        self.odd_y = odd_y
        self.investment = investment

    @staticmethod
    def american_to_decimal(american_odd: int) -> float:
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

    @staticmethod
    def american_to_implied(american_odd: int) -> float:
        """
        Convert American odds to implied probability.

        Parameters:
        american_odd (int): The American odds.

        Returns:
        float: The implied probability.
        """
        implied_odds = 1 / Arbitrage.american_to_decimal(american_odd)
        return implied_odds

    def is_arbitrage(self) -> bool:
        """
        Check if the given odds represent an arbitrage opportunity.

        Returns:
        bool: True if there is an arbitrage opportunity, False otherwise.
        """
        arbitrage_pct = self.american_to_implied(self.odd_x) + self.american_to_implied(self.odd_y)
        return arbitrage_pct < 1

    def unbiased_arbitrage(self) -> tuple[float, float] | None:
        """
        Calculate wagers for unbiased arbitrage.

        Parameters:
        None

        Returns:
        tuple: The amounts to wager on odd_x and odd_y respectively, rounded to 2 decimal places.
        None: If no arbitrage opportunity exists.
        """
        if self.is_arbitrage():
            arbitrage_pct = self.american_to_implied(self.odd_x) + self.american_to_implied(self.odd_y)
            wager_x = (self.investment * self.american_to_implied(self.odd_x)) / arbitrage_pct
            wager_y = (self.investment * self.american_to_implied(self.odd_y)) / arbitrage_pct
            return round(wager_x, 2), round(wager_y, 2)
        else:
            logging.warning("Not a valid arbitrage")
            return None

    def biased_arbitrage(self, preferred_index=0) -> tuple[float, float] | None:
        """
        Calculate wagers for biased arbitrage.

        Parameters:
        preferred_index (int): The index of the preferred set of odds (0 for odd_x, 1 for odd_y).

        Returns:
        tuple: The amounts to wager on preferred_odd and cover_odd respectively, rounded to 2 decimal places.
        None: If no arbitrage opportunity exists.
        """
        cover_list = [
            self.odd_x,
            self.odd_y
        ]

        del cover_list[preferred_index]

        if self.is_arbitrage():
            total_cover_wager = 0
            for odd in cover_list:
                cover_wager = self.american_to_implied(odd) * self.investment
                total_cover_wager += cover_wager
            preferred_wager = self.investment - total_cover_wager
            return round(preferred_wager, 2), round(cover_wager, 2)
        else:
            logging.warning("Not a valid arbitrage")
            return None

    @staticmethod
    def return_on_investment(net_return: float, investment: float) -> float:
        """
        Calculate the Return on Investment (ROI).

        Parameters:
        net_return (float): The net return from the investment.
        investment (float): The initial investment amount.

        Returns:
        float: The ROI as a ratio of net return to investment.
        """
        return net_return / investment

    @staticmethod
    def net_return(stake: float, odds: int) -> float:
        """
        Calculate the net return from a stake based on American odds.

        Parameters:
        stake (float): The amount of money staked.
        odds (int): The American odds for the bet.

        Returns:
        float: The net return from the stake.
        """
        return stake * Arbitrage.american_to_decimal(odds)

    def biased_prob_threshold(self) -> tuple[float, float] | None:
        """
        Calculate the probability threshold of choosing biased over unbiased arbitrage strategy.

        Parameters:
        None

        Returns:
        tuple: A tuple containing the probabilities (as ratios) of choosing the biased arbitrage for
               each set of odds (biased_prob_a, biased_prob_b).
        None: If no arbitrage opportunity exists.
        """
        if self.is_arbitrage():
            unbiased_stake = self.unbiased_arbitrage()[0]
            unbiased_return = self.net_return(unbiased_stake, self.odd_x)
            unbiased_roi = self.return_on_investment(unbiased_return, self.investment)

            biased_stake_a = self.biased_arbitrage(0)[0]
            biased_return_a = self.net_return(biased_stake_a, self.odd_x)
            biased_roi_a = self.return_on_investment(biased_return_a, self.investment)

            biased_stake_b = self.biased_arbitrage(1)[0]
            biased_return_b = self.net_return(biased_stake_b, self.odd_y)
            biased_roi_b = self.return_on_investment(biased_return_b, self.investment)

            biased_prob_a = unbiased_roi / biased_roi_a
            biased_prob_b = unbiased_roi / biased_roi_b

            return biased_prob_a, biased_prob_b
        else:
            logging.warning("Not a valid arbitrage")
            return None

class ThreeWayArbitrage(Arbitrage):
    """
    A class for handling arbitrage calculations with three odd bets.

    Attributes:
    odd_x (int): The first set of American odds.
    odd_y (int): The second set of American odds.
    odd_z (int): The third set of American odds.
    investment (float): The total amount to invest.
    """

    def __init__(self, odd_x, odd_y, odd_z, investment):
        super().__init__(odd_x, odd_y, investment) 
        self.odd_z = odd_z

    def is_arbitrage(self) -> bool:
        """
        Check if the given odds represent an arbitrage opportunity for three bets.

        Returns:
        bool: True if there is an arbitrage opportunity, False otherwise.
        """
        implied_sum = (
            self.american_to_implied(self.odd_x) +
            self.american_to_implied(self.odd_y) +
            self.american_to_implied(self.odd_z)
        )
        return implied_sum < 1

    def unbiased_arbitrage(self) -> tuple[float, float, float] | None:
        """
        Calculate wagers for three-way arbitrage.

        Parameters:
        None

        Returns:
        tuple: The amounts to wager on odd_x, odd_y, and odd_z respectively, rounded to 2 decimal places.
        None: If no arbitrage opportunity exists.
        """
        if self.is_arbitrage():
            implied_x = self.american_to_implied(self.odd_x)
            implied_y = self.american_to_implied(self.odd_y)
            implied_z = self.american_to_implied(self.odd_z)

            total_implied = implied_x + implied_y + implied_z

            wager_x = (self.investment * implied_x) / total_implied
            wager_y = (self.investment * implied_y) / total_implied
            wager_z = (self.investment * implied_z) / total_implied

            return round(wager_x, 2), round(wager_y, 2), round(wager_z, 2)
        else:
            logging.warning("Not a valid arbitrage")
            return None

    def biased_arbitrage(self, preferred_index=0) -> tuple[float, float, float] | None:
        """
        Calculate wagers for biased arbitrage.

        Parameters:
        preferred_index (int): The index of the preferred set of odds (0 for odd_x, 1 for odd_y).

        Returns:
        tuple: The amounts to wager on preferred_odd and cover_odd respectively, rounded to 2 decimal places.
        None: If no arbitrage opportunity exists.
        """
        cover_list = [
            self.odd_x,
            self.odd_y,
            self.odd_z
        ]

        cover_wagers = []

        _ = cover_list.pop(preferred_index)

        if self.is_arbitrage():
            total_cover_wager = 0
            for odd in cover_list:
                cover_wager = self.american_to_implied(odd) * self.investment
                total_cover_wager += cover_wager
                cover_wagers.append(cover_wager)
            preferred_wager = self.investment - total_cover_wager
            cover_wagers.insert(preferred_index, preferred_wager)
            return round(cover_wagers[0], 2), round(cover_wagers[1], 2), round(cover_wagers[2], 2)
        else:
            logging.warning("Not a valid arbitrage")
            return None

if __name__ == "__main__":
    # Example usage for two-way arbitrage
    two_way = Arbitrage(150, -125, 500)
    print("Two-Way Arbitrage:")
    print("Unbiased:", two_way.unbiased_arbitrage())
    for i in range(2):
        print("Biased:", two_way.biased_arbitrage(i))
    print("Biased Prob Threshold:", two_way.biased_prob_threshold())

    # Example usage for three-way arbitrage
    three_way = ThreeWayArbitrage(250, 300, 200, 500)
    print("Three-Way Arbitrage:")
    print("Three-Way Wagers:", three_way.unbiased_arbitrage())
    for i in range(3):
        print("Biased:", three_way.biased_arbitrage(i))