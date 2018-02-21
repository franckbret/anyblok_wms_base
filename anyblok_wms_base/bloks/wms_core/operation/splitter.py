# -*- coding: utf-8 -*-
# This file is a part of the AnyBlok / WMS Base project
#
#    Copyright (C) 2018 Georges Racinet <gracinet@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime

from anyblok import Declarations
from anyblok.column import Boolean

from anyblok_wms_base.exceptions import (
    OperationError,
    OperationQuantityError,
)

Mixin = Declarations.Mixin


@Declarations.register(Mixin)
class WmsSingleGoodsSplitterOperation(Mixin.WmsSingleGoodsOperation):
    """Mixin for operations on a single record of Goods that can split.

    In case the operation's quantity is less than in the Goods record,
    a split will be inserted properly in history.

    The 'partial' column is used to track whether the operation's
    original Goods have greater quantity than the operation's, i.e., whether
    a split should occur or have occured, because once the split is done,
    this can't be deduced from the quantities involved any more.
    """

    partial = Boolean(label="Operation induced a split")

    def specific_repr(self):
        return ("goods={self.goods!r}, "
                "quantity={self.quantity}").format(self=self)

    def check_execute_conditions(self):
        goods = self.goods
        if self.quantity != goods.quantity:
            raise OperationQuantityError(
                self,
                "Can't execute planned for a different quantity {qty} "
                "than held in goods {goods} "
                "(which have quantity={goods.quantity}). "
                "For lesser quantities, a split should have occured first ",
                goods=goods, quantity=self.quantity)
        if not self.partial:
            # if partial, then it's normal that self.goods be in 'future'
            # state: the current Operation execution will complete the split
            super(WmsSingleGoodsSplitterOperation,
                  self).check_execute_conditions()

    @classmethod
    def create(cls, state='planned', follows=None, goods=None, quantity=None,
               dt_execution=None, dt_start=None, **kwargs):
        """Main method for creation of operations

        This is entirely overridden from :class:`Operation`, because
        in partial cases, it's simpler to create directly the split, then
        the current operation.

        TODO provide another hook to limit duplication
        """
        cls.forbid_follows_in_create(follows, kwargs)
        if dt_execution is None:
            if state == 'done':
                dt_execution = datetime.now()
            else:
                raise OperationError(
                    cls,
                    "Creation in state {state!r} requires the "
                    "'dt_execution' kwarg (date and time when "
                    "it's supposed to be done).",
                    state=state)
        cls.check_create_conditions(state, dt_execution,
                                    goods=goods, quantity=quantity,
                                    **kwargs)
        follows = cls.find_parent_operations(goods=goods, **kwargs)
        partial = quantity < goods.quantity
        if partial:
            Split = cls.registry.Wms.Operation.Split
            split = Split.create(goods=goods, quantity=quantity, state=state,
                                 dt_execution=dt_execution)
            follows = [split]
            goods = split.get_outcome()

        op = cls.insert(state=state, goods=goods, quantity=quantity,
                        dt_execution=dt_execution, partial=partial, **kwargs)
        op.follows.extend(follows)
        op.after_insert()
        return op

    def execute_planned(self):
        if self.partial:
            split_op = self.follows[0]
            split_op.execute(dt_execution=self.dt_execution)
        self.execute_planned_after_split()
        self.registry.flush()