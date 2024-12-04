package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

func parseInput(filename string) [][]rune {
	content, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(content), "\n")
	entries := make([][]rune, 0)
	for _, line := range lines {
		entries = append(entries, []rune(line))
	}

	return entries
}

type Point struct {
	X int
	Y int
}

func (p Point) String() string {
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

type Selection struct {
	Start     Point
	End       Point
	direction string
}

func (s Selection) String() string {
	return fmt.Sprintf("Start: %s, End: %s, Direction: %s", s.Start, s.End, s.direction)
}
func matrixWordSearch(matrix [][]rune, word string) []Selection {
	wordLen := len(word)
	matches := make([]Selection, 0)
	for i := 0; i < len(matrix); i++ {
		for j := 0; j < len(matrix[i]); j++ {
			if matrix[i][j] == rune(word[0]) {
				// check right
				if j+wordLen-1 < len(matrix[i]) {
					wordCheck := matrix[i][j : j+wordLen]
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i, j + wordLen - 1}, "right"})
					}
				}
				// check down
				if i+wordLen-1 < len(matrix) {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i+k][j])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i + wordLen - 1, j}, "down"})
					}
				}
				// check left
				if j >= wordLen-1 {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i][j-k])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i, j - wordLen + 1}, "left"})
					}
				}
				// check up
				if i >= wordLen-1 {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i-k][j])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i - wordLen + 1, j}, "up"})
					}
				}
				// check diagonal right down
				if i+wordLen-1 < len(matrix) && j+wordLen-1 < len(matrix[i]) {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i+k][j+k])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i + wordLen - 1, j + wordLen - 1}, "right down"})
					}
				}
				// check diagonal left down
				if i+wordLen-1 < len(matrix) && j >= wordLen-1 {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i+k][j-k])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i + wordLen - 1, j - wordLen + 1}, "left down"})
					}
				}
				// check diagonal left up
				if i >= wordLen-1 && j >= wordLen-1 {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i-k][j-k])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i - wordLen + 1, j - wordLen + 1}, "left up"})
					}
				}
				// check diagonal right up
				if i >= wordLen-1 && j+wordLen-1 < len(matrix[i]) {
					wordCheck := make([]rune, 0, wordLen)
					for k := 0; k < wordLen; k++ {
						wordCheck = append(wordCheck, matrix[i-k][j+k])
					}
					if word == string(wordCheck) {
						matches = append(matches, Selection{Point{i, j}, Point{i - wordLen + 1, j + wordLen - 1}, "right up"})
					}
				}
			}
		}
	}
	return matches
}

func part1(input [][]rune) {
	matches := matrixWordSearch(input, "XMAS")
	fmt.Println(len(matches))

}
func part2(input [][]rune) {
	word := "MAS"
	masMatches := matrixWordSearch(input, word)
	crossMatches := make([][]Selection, 0)
	diagonalMatches := make([]Selection, 0)
	// find all diagonal matches
	for _, match := range masMatches {
		if match.Start.X == match.End.X || match.Start.Y == match.End.Y {
			continue
		}
		diagonalMatches = append(diagonalMatches, match)
	}

	// check if is a cross
	for _, match1 := range diagonalMatches {
		for _, match2 := range diagonalMatches {
			if match1 == match2 {
				continue
			}

			midX1 := int(math.Max(float64(match1.Start.X), float64(match1.End.X)) - 1)
			midY1 := int(math.Max(float64(match1.Start.Y), float64(match1.End.Y)) - 1)

			midX2 := int(math.Max(float64(match2.Start.X), float64(match2.End.X)) - 1)
			midY2 := int(math.Max(float64(match2.Start.Y), float64(match2.End.Y)) - 1)

			if midX1 == midX2 && midY1 == midY2 {
				crossMatches = append(crossMatches, []Selection{match1, match2})
				break
			}
		}
	}

	fmt.Println(len(crossMatches) / 2)
}

func main() {
	input := parseInput(os.Args[1])
	part1(input)
	part2(input)
}
