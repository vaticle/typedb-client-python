#
# Copyright (C) 2022 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import annotations
from abc import ABC
from datetime import datetime
from typing import Optional, Iterator

import typedb_protocol.common.concept_pb2 as concept_proto

from typedb.api.concept.thing.attribute import Attribute
from typedb.api.concept.type.thing_type import ThingType
from typedb.api.concept.value.value import Value
from typedb.api.connection.transaction import Transaction
from typedb.common.rpc.request_builder import attribute_get_owners_req
from typedb.concept.proto import concept_proto_builder, concept_proto_reader
from typedb.concept.thing.thing import _Thing

from typedb.typedb_client_python import Concept, attribute_get_type, attribute_get_value, attribute_get_owners

from typedb.concept.type.attribute_type import _AttributeType
from typedb.concept.value.value import _Value


class _Attribute(Attribute, _Thing, ABC):

    # def as_attribute(self) -> "Attribute":
    #     return self

    def get_type(self) -> _AttributeType:
        return _AttributeType(attribute_get_type(self._concept))

    def get_value(self) -> _Value:
        return _Value(attribute_get_value(self._concept))

    def get_owners(self, transaction: Transaction, owner_type: Optional[ThingType] = None) -> Iterator[_Thing]:
        return (_Thing(item) for item in attribute_get_owners(self.native_transaction(transaction), self._concept, owner_type.native_object()))


# class _BooleanAttribute(BooleanAttribute, _Attribute):
#
#     def __init__(self, iid: str, is_inferred: bool, type_: BooleanAttributeType, value: bool):
#         super(_BooleanAttribute, self).__init__(iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     @staticmethod
#     def of(thing_proto: concept_proto.Thing):
#         return _BooleanAttribute(concept_proto_reader.iid(thing_proto.iid), thing_proto.inferred, concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.boolean)
#
#     def get_type(self) -> "BooleanAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteBooleanAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _RemoteBooleanAttribute(RemoteBooleanAttribute, _RemoteAttribute):
#
#     def __init__(self, transaction, iid: str, is_inferred: bool, type_, value: bool):
#         super(_RemoteBooleanAttribute, self).__init__(transaction, iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     def get_type(self) -> "BooleanAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteBooleanAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _LongAttribute(LongAttribute, _Attribute):
#
#     def __init__(self, iid: str, is_inferred: bool, type_: LongAttributeType, value: int):
#         super(_LongAttribute, self).__init__(iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     @staticmethod
#     def of(thing_proto: concept_proto.Thing):
#         return _LongAttribute(concept_proto_reader.iid(thing_proto.iid), thing_proto.inferred, concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.long)
#
#     def get_type(self) -> "LongAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteLongAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _RemoteLongAttribute(RemoteLongAttribute, _RemoteAttribute):
#
#     def __init__(self, transaction, iid: str, is_inferred: bool, type_, value: int):
#         super(_RemoteLongAttribute, self).__init__(transaction, iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     def get_type(self) -> "LongAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteLongAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _DoubleAttribute(DoubleAttribute, _Attribute):
#
#     def __init__(self, iid: str, is_inferred: bool, type_: DoubleAttributeType, value: float):
#         super(_DoubleAttribute, self).__init__(iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     @staticmethod
#     def of(thing_proto: concept_proto.Thing):
#         return _DoubleAttribute(concept_proto_reader.iid(thing_proto.iid), thing_proto.inferred, concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.double)
#
#     def get_type(self) -> "DoubleAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteDoubleAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _RemoteDoubleAttribute(RemoteDoubleAttribute, _RemoteAttribute):
#
#     def __init__(self, transaction, iid: str, is_inferred: bool, type_: DoubleAttributeType, value: float):
#         super(_RemoteDoubleAttribute, self).__init__(transaction, iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     def get_type(self) -> "DoubleAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteDoubleAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _StringAttribute(StringAttribute, _Attribute):
#
#     def __init__(self, iid: str, is_inferred: bool, type_: StringAttributeType, value: str):
#         super(_StringAttribute, self).__init__(iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     @staticmethod
#     def of(thing_proto: concept_proto.Thing):
#         return _StringAttribute(concept_proto_reader.iid(thing_proto.iid), thing_proto.inferred, concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.string)
#
#     def get_type(self) -> "StringAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteStringAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _RemoteStringAttribute(RemoteStringAttribute, _RemoteAttribute):
#
#     def __init__(self, transaction, iid: str, is_inferred: bool, type_: StringAttributeType, value: str):
#         super(_RemoteStringAttribute, self).__init__(transaction, iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     def get_type(self) -> "StringAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteStringAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _DateTimeAttribute(DateTimeAttribute, _Attribute):
#
#     def __init__(self, iid: str, is_inferred: bool, type_: DateTimeAttributeType, value: datetime):
#         super(_DateTimeAttribute, self).__init__(iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     @staticmethod
#     def of(thing_proto: concept_proto.Thing):
#         return _DateTimeAttribute(concept_proto_reader.iid(thing_proto.iid), thing_proto.inferred, concept_proto_reader.attribute_type(thing_proto.type), datetime.utcfromtimestamp(float(thing_proto.value.date_time) / 1000.0))
#
#     def get_type(self) -> "DateTimeAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteDateTimeAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
#
#
# class _RemoteDateTimeAttribute(RemoteDateTimeAttribute, _RemoteAttribute):
#
#     def __init__(self, transaction, iid: str, is_inferred: bool, type_: DateTimeAttributeType, value: datetime):
#         super(_RemoteDateTimeAttribute, self).__init__(transaction, iid, is_inferred)
#         self._type = type_
#         self._value = value
#
#     def get_type(self) -> "DateTimeAttributeType":
#         return self._type
#
#     def get_value(self):
#         return self._value
#
#     def as_remote(self, transaction):
#         return _RemoteDateTimeAttribute(transaction, self.get_iid(), self.is_inferred(), self.get_type(), self.get_value())
