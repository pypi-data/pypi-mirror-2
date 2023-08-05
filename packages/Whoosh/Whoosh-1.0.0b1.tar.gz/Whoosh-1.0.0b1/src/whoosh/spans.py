#===============================================================================
# Copyright 2010 Matt Chaput
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================

from whoosh.matching import (Matcher, BiMatcher, WrappingMatcher,
                             IntersectionMatcher, ReadTooFar, NullMatcher)

class SpanMatcher(object):
    def spans(self):
        """Returns a list of ``(startpos, endpos)`` tuples representing the
        matching spans in the current document.
        """
        raise NotImplementedError


class SpanTerm(WrappingMatcher, SpanMatcher):
    def spans(self):
        return [(pos, pos) for pos in self.value_as("positions")]


class RelationSpan(WrappingMatcher, SpanMatcher):
    @staticmethod
    def before(aspans, bspans):
        if not bspans:
            return []
        front = bspans[0][0]
        return [span for span in aspans if span[1] < front]
    
    @staticmethod
    def after(aspans, bspans):
        if not bspans:
            return []
        back = bspans[-1][1]
        return [span for span in aspans if span[0] > back]
    
    @staticmethod
    def within(aspans, bspans):
        if not bspans:
            return []
        results = []
        for span in aspans:
            start, end = span
            for bstart, bend in bspans:
                if start >= bstart and end <= bend:
                    results.append(span)
        return results
    
    @staticmethod
    def without(aspans, bspans):
        if not bspans:
            return aspans
        results = []
        for span in aspans:
            start, end = span
            for bstart, bend in bspans:
                if end < bstart or start > bend:
                    results.append(span)
        return results
    
    @staticmethod
    def overlaps(aspans, bspans):
        if not bspans:
            return []
        results = []
        for span in aspans:
            start, end = span
            for bstart, bend in bspans:
                if ((end >= bstart and end <= bend)
                    or (start >= bstart and start <= bend)):
                    results.append(span)
        return results
    
    def __init__(self, a, b, fn):
        super(RelationSpan, self).__init__(IntersectionMatcher(a, b))
        self.a = a
        self.b = b
        self.fn = fn
        self._find_next()

    def is_active(self):
        return self.child.is_active()

    def replace(self):
        if not self.is_active(): return NullMatcher()
        return self
    
    def supports_quality(self):
        return self.a.supports_quality()
    
    def quality(self):
        return self.a.quality()
    
    def block_quality(self):
        return self.a.block_quality()
    
    def spans(self):
        return self._spans

    def _find_next(self):
        a = self.a
        b = self.b
        child = self.child
        fn = self.fn
        
        spans = fn(a.spans(), b.spans())
        while child.is_active() and not spans:
            child.next()
            if child.is_active():
                spans = fn(a.spans(), b.spans())
        self._spans = spans

    def skip_to(self, id):
        if not self.is_active(): raise ReadTooFar
        ra = self.a.skip_to(id)
        rb = self.b.skip_to(id)
        rn = False
        if self.a.is_active() and self.b.is_active():
            rn = self._find_next()
        return ra or rb or rn
    
    def next(self):
        self.isect.next()
        self._find_next()








    
