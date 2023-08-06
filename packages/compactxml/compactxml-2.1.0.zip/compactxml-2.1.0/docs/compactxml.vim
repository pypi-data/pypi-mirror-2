" Vim syntax file
" Language: compactxml
" Maintainer: John Krukoff <python@cultist.org>
" Latest Revision: Thu Aug 12 14:44:33 MDT 2010

if exists( "b:current_syntax" )
	finish
endif

syn match compactEscapeDouble /""/ contained
syn match compactEscapeSingle /''/ contained
syn match compactNamespace /:/ contained

syn region compactLiteral start=/\S/ end=/\s\|$/ oneline nextgroup=compactLiteral skipwhite
syn region compactQuotedLiteral start=/"/ skip=/""/ end=/"/ oneline keepend contains=compactEscapeDouble nextgroup=compactLiteral skipwhite
syn region compactQuotedLiteral start=/'/ skip=/''/ end=/'/ oneline keepend contains=compactEscapeSingle nextgroup=compactLiteral skipwhite
syn cluster compactLiterals contains=compactLiteral,compactQuotedLiteral

syn region compactInlineLiteral start=/\S/ end=/\s\|$/ oneline nextgroup=@compactInlineLiterals skipwhite
syn region compactInlineQuotedLiteral start=/"/ skip=/""/ end=/"/ oneline keepend contains=compactEscapeDouble nextgroup=@compactInlineLiterals skipwhite
syn region compactInlineQuotedLiteral start=/'/ skip=/''/ end=/'/ oneline keepend contains=compactEscapeSingle nextgroup=@compactInlineLiterals skipwhite
syn match compactInlineAssign /=/ nextgroup=compactInlineLiteral,compactInlineQuotedLiteral skipwhite
syn match compactInlineNamedLiteral /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?\s*=\@=/ contains=compactNamespace nextgroup=compactInlineAssign skipwhite
syn match compactInlinePrefix /#\|@/ nextgroup=compactInlineNamedLiteral skipwhite
syn cluster compactInlineLiterals contains=compactInlineLiteral,compactInlineQuotedLiteral,compactInlineNamedLiteral,compactInlinePrefix

syn match compactName /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?/ contains=compactNamespace skipwhite
syn match compactTag /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?/ contains=compactNamespace nextgroup=@compactLiterals skipwhite
syn match compactElement /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?/ contains=compactNamespace nextgroup=@compactInlineLiterals skipwhite
syn match compactMacro /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?/ contains=compactNamespace nextgroup=@compactInlineLiterals skipwhite
syn match compactMacroDefine /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?/ contains=compactNamespace nextgroup=@compactInlineLiterals skipwhite
syn match compactGroupDefine /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?/ contains=compactNamespace skipwhite
syn match compactAssign /=/ nextgroup=@compactLiterals skipwhite
syn match compactNamedLiteral /[0-9a-zA-Z_-]\+\(:[0-9a-zA-Z_-]\+\)\?\s*=\@=/ nextgroup=compactAssign skipwhite

syn match compactCommandOther /comment\|contents\|default\|encoding\|load\|indent\|variable/ nextgroup=@compactLiterals skipwhite
syn match compactCommandMacro /element/ nextgroup=compactMacroDefine skipwhite
syn match compactCommandGroup /attribute/ nextgroup=compactGroupDefine skipwhite
syn cluster compactCommands contains=compactCommandOther,compactCommandMacro,compactCommandGroup

syn match compactMacro /^\s*/ nextgroup=compactMacro skipwhite
syn match compactPrefix /^\s*</ nextgroup=compactElement skipwhite
syn match compactPrefix /^\s*<!/ nextgroup=@compactLiterals skipwhite
syn match compactPrefix /^\s*<?/ nextgroup=compactTag skipwhite
syn match compactPrefix /^\s*#/ nextgroup=compactNamedLiteral,@compactLiterals skipwhite
syn match compactPrefix /^\s*@/ nextgroup=compactNamedLiteral,compactTag skipwhite
syn match compactPrefix /^\s*@@/ nextgroup=compactName skipwhite
syn match compactPrefix /^\s*"/ nextgroup=@compactLiterals skipwhite
syn match compactPrefix /^\s*!/ nextgroup=@compactLiterals skipwhite
syn match compactCommand /^\s*?/ nextgroup=@compactCommands skipwhite
syn match compactContinuation /^\s*\\/ nextgroup=@compactLiterals skipwhite
syn match compactContinuation /^\s*+/ nextgroup=@compactLiterals skipwhite
syn match compactContinuation /^\s*\$/ nextgroup=compactName skipwhite

if has( "spell" )
	syn cluster Spell contains=@compactLiterals,compactInlineLiteral,compactInlineQuotedLiteral
	syn spell notoplevel
endif

let b:current_syntax = "compactxml"

hi def link compactPrefix		Statement
hi def link compactInlinePrefix		Statement
hi def link compactCommand		PreProc
hi def link compactCommandOther		PreProc
hi def link compactCommandMacro		PreProc
hi def link compactCommandGroup		PreProc
hi def link compactMacroDefine		Identifier
hi def link compactGroupDefine		Identifier
hi def link compactContinuation		Operator
hi def link compactAssign		Keyword
hi def link compactInlineAssign		Keyword
hi def link compactName			NONE
hi def link compactNamespace		Keyword
hi def link compactTag			NONE
hi def link compactNamedLiteral		NONE
hi def link compactQuotedLiteral	String
hi def link compactInlineQuotedLiteral	String
hi def link compactLiteral		NONE
hi def link compactEscapeDouble		SpecialChar
hi def link compactEscapeSingle		SpecialChar
