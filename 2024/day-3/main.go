package main

import (
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
	"unicode"
)

func parseInput(filename string) string {
	content, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return string(content)
}

type Mul struct {
	A int
	B int
}

func (m Mul) String() string {
	return "mul(" + strconv.Itoa(m.A) + "," + strconv.Itoa(m.B) + ")"
}

func part1(input string) {
	parts := make([]string, 0)
	var part string
	for _, char := range input {
		part += string(char)
		if char == ')' {
			parts = append(parts, part)
			part = ""
		}
	}
	// filter and map parts
	validParts := make([]Mul, 0)
	r := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	for _, part := range parts {
		matches := r.FindStringSubmatch(part)
		if len(matches) == 3 {
			n, _ := strconv.Atoi(matches[1])
			m, _ := strconv.Atoi(matches[2])
			validParts = append(validParts, Mul{n, m})
		}
	}

	sum := 0
	for _, part := range validParts {
		sum += part.A * part.B
	}
	println(sum)
}

type TokenType int

const (
	TOKEN_MUL  = iota // mul keyword
	TOKEN_LPAR        // (
	TOKEN_RPAR        // )
	TOKEN_COMA        // ,
	TOKEN_NUM         // numeric value

	TOKEN_DONT // don't keyword
	TOKEN_DO   // do keyword

	TOKEN_EOF // end of input
	TOKEN_INVALID
)

func (t TokenType) String() string {
	switch t {
	case TOKEN_MUL:
		return "mul"
	case
		TOKEN_LPAR:
		return "("
	case
		TOKEN_RPAR:
		return ")"
	case
		TOKEN_COMA:
		return ","
	case
		TOKEN_NUM:
		return "num"
	case
		TOKEN_DONT:
		return "don't"
	case
		TOKEN_DO:
		return "do"
	}
	return ""
}

type Token struct {
	TokenType TokenType
	Value     string
	Position  int
}

func (t Token) String() string {
	return t.Value
}

type Lexer struct {
	input   string
	pos     int
	current byte
}

func NewLexer(input string) *Lexer {
	l := &Lexer{
		input: input,
	}
	if len(input) > 0 {
		l.current = input[0]
	}

	return l
}

func (l *Lexer) advance() {
}

func (l *Lexer) nextToken() Token {
	for l.pos < len(l.input) && unicode.IsSpace(rune(l.input[l.pos])) {
		l.pos++
	}

	if l.pos >= len(l.input) {
		return Token{TOKEN_EOF, "", l.pos}
	}

	switch l.input[l.pos] {
	case '(':
		l.pos++
		return Token{TOKEN_LPAR, "(", l.pos}
	case ')':
		l.pos++
		return Token{TOKEN_RPAR, ")", l.pos}
	case ',':
		l.pos++
		return Token{TOKEN_COMA, ",", l.pos}
	}

	if unicode.IsDigit(rune(l.input[l.pos])) {
		start := l.pos
		for l.pos < len(l.input) && unicode.IsDigit(rune(l.input[l.pos])) {
			l.pos++
		}
		// only accept numbers of length 1-3
		if l.pos-start > 3 {
			return Token{TOKEN_INVALID, "", l.pos}
		}
		return Token{TOKEN_NUM, l.input[start:l.pos], start}
	}

	keywords := map[string]TokenType{
		"mul":   TOKEN_MUL,
		"don't": TOKEN_DONT,
		"do":    TOKEN_DO,
	}

	for k, v := range keywords {
		if strings.HasPrefix(l.input[l.pos:], k) {
			l.pos += len(k)
			return Token{v, k, l.pos}
		}
	}

	l.pos++
	return Token{TOKEN_INVALID, "", l.pos}
}

func (l *Lexer) Parse() []Token {
	tokens := make([]Token, 0)
	for {
		token := l.nextToken()
		tokens = append(tokens, token)
		if token.TokenType == TOKEN_EOF {
			break
		}
	}

	// filter out invalid tokens
	// only accept pattern mul(NUM,NUM)
	validTokens := make([]Token, 0)
	for i, token := range tokens {
		switch token.TokenType {
		case TOKEN_MUL:

			if i+4 < len(tokens)-1 && tokens[i+1].TokenType == TOKEN_LPAR && tokens[i+2].TokenType == TOKEN_NUM && tokens[i+3].TokenType == TOKEN_COMA && tokens[i+4].TokenType == TOKEN_NUM && tokens[i+5].TokenType == TOKEN_RPAR {
				validTokens = append(validTokens, token, tokens[i+2], tokens[i+4])
			}
		case TOKEN_DONT:
			if i+2 < len(tokens)-1 && tokens[i+1].TokenType == TOKEN_LPAR && tokens[i+2].TokenType == TOKEN_RPAR {
				validTokens = append(validTokens, token)
			}

		case TOKEN_DO:
			if i+2 < len(tokens)-1 && tokens[i+1].TokenType == TOKEN_LPAR && tokens[i+2].TokenType == TOKEN_RPAR {
				validTokens = append(validTokens, token)
			}
		}
	}

	return validTokens
}

func calculate(tokens []Token) int {
	sum := 0
	active := true
	for i, t := range tokens {
		if t.TokenType == TOKEN_DONT {
			active = false
		}
		if t.TokenType == TOKEN_DO {
			active = true
		}

		if t.TokenType == TOKEN_MUL && active {
			a, _ := strconv.Atoi(tokens[i+1].Value)
			b, _ := strconv.Atoi(tokens[i+2].Value)

			sum += a * b
		}
	}…
	return sum
}

func main() {
	input := parseInput(os.Args[1])

	lexer := NewLexer(input)
	tokens := lexer.Parse()

	part1(input)
	sum := calculate(tokens)
	log.Println(sum)
}
