# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from yay.nodes import Node, Boxed, Sequence
from yay.context import Context

class ForEach(Node):

    def __init__(self, root, value, args):
        self.root = root
        self.value = value

        self.lookup = args[1]
        self.alias = args[0].strip()

    def semi_resolve(self, context):
        resolved = []
        for item in self.lookup.semi_resolve(context):
            newctx = Context(context, {self.alias: item})
            resolved.append(self.value.resolve(newctx))
        return Sequence(list(Boxed(x) for x in resolved))

    def resolve(self, context):
        return self.semi_resolve(context).resolve(context)

    def walk(self, context):
        yield self.lookup
        yield self.value

