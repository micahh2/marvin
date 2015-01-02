from .searchprovider import SearchProvider
from .searchresult import SearchResult
from sympy import *
import re

class SymPySearchProvider(SearchProvider):

    @property
    def title(self):
        return "SymPy Evaluation"

    def sanitize_input(self, q):
        """Santize in the input"""
        badwords = [r"\bimport\b", r"\bos\(b" r"\blambda\b", r"\bsystem\b", r"\b__.+__\b"]
        while sum([re.match(i, q) != None for i in badwords]) > 0:
            for i in badwords:
                q = re.sub(i, "", q)
        return q

    def routine(self, q):
        """Check if there is a simple mathimatical solution."""
        q = self.sanitize_input(q)
        try:
            expression = sympify(q).evalf()
            self.result = SearchResult("$$" + latex(expression) + "$$", confidence=.75)
            if str(expression).lower().strip() == q.lower().strip():
                self.result.confidence = 0;
        except (SympifyError) as e:
            self.result = SearchResult("Poor formed expression")
