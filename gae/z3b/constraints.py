# Copyright (c) 2013 The SAYCBridge Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from z3b.model import expr_for_suit
import z3b.model as model


class Constraint(object):
    def expr(self, history, call):
        pass


class MinimumCombinedLength(Constraint):
    def __init__(self, min_count):
        self.min_count = min_count

    def expr(self, history, call):
        suit = call.strain
        partner_promised_length = history.partner.min_length(suit)
        implied_length = max(self.min_count - partner_promised_length, 0)
        return expr_for_suit(suit) >= implied_length


class MinimumCombinedPoints(Constraint):
    def __init__(self, min_points):
        self.min_points = min_points

    def expr(self, history, call):
        return model.points >= max(0, self.min_points - history.partner.min_points)


class MinLength(Constraint):
    def __init__(self, min_length):
        self.min_length = min_length

    def expr(self, history, call):
        return expr_for_suit(call.strain) >= self.min_length


class ThreeOfTheTopFive(Constraint):
    def expr(self, history, call):
        return (
            model.three_of_the_top_five_clubs,
            model.three_of_the_top_five_diamonds,
            model.three_of_the_top_five_hearts,
            model.three_of_the_top_five_spades,
        )[call.strain]