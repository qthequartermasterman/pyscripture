from __future__ import annotations

import pydantic
from typing import List, Any, Dict


class Audio(pydantic.BaseModel):
    """Audio for a scripture chapter or verse."""

    mediaUrl: str
    variant: str


class Meta(pydantic.BaseModel):
    """Metadata about a scripture chapter or verse."""

    archived: bool
    title: str
    canonicalUrl: str
    contentType: str  # "text/html"
    audio: List[Audio]
    pageAttributes: Any
    # "pageAttributes": {
    #     "data-asset-id": "34085354c9883ef35ff0623e36634ee00725eca2",
    #     "data-aid": "128345022",
    #     "data-aid-version": "6",
    #     "data-content-type": "chapter",
    #     "data-uri": "/scriptures/bofm/1-ne/6",
    #     "lang": "eng",
    #     "data-orig-id": "34085354c9883ef35ff0623e36634ee00725eca2",
    #     "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    # },
    scopedClassName: str  # "classic-scripture"


class ReferenceUri(pydantic.BaseModel):
    type: str
    href: str
    text: str


class Footnote(pydantic.BaseModel):
    id: str
    marker: str = ''
    pid: str = ''
    context: str = ''
    text: str
    referenceUris: List[ReferenceUri] = pydantic.Field(default_factory=list)

    def uris(self) -> List[str]:
        return [uri.href for uri in self.referenceUris]


class Content(pydantic.BaseModel):
    head: Any
    body: str
    footnotes: Dict[str, Footnote]


class ScriptureStudyContent(pydantic.BaseModel):
    """Content for a scripture chapter or verse."""

    meta: Meta
    content: Content
    pids: Any
    tableOfContentsUri: str
    uri: str
    verified: bool


class ContentApiContent(pydantic.BaseModel):
    id: str
    markup: str
    displayId: str = ''


class ContentApiResponse(pydantic.BaseModel):
    content: List[ContentApiContent]
    headline: str
    publication: str
    referenceURIDisplayText: str | Any
    referenceURI: str | Any
    type: str
    uri: str
    image: Any
    idNotationUri: str | Any = ''
