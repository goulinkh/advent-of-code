package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

type OrderRule struct {
	left  int
	right int
}

func (o OrderRule) String() string {
	return strconv.Itoa(o.left) + "|" + strconv.Itoa(o.right)
}

type PrintOrder []int

func parseInput(filename string) ([]OrderRule, []PrintOrder) {
	content, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(content), "\n")

	rules := make([]OrderRule, 0)
	var printOrderStartLine int
	for i, line := range lines {
		if line == "" {
			printOrderStartLine = i + 1
			break
		}
		parts := strings.Split(line, "|")
		left, err := strconv.Atoi(parts[0])
		if err != nil {
			panic(err)
		}
		right, err := strconv.Atoi(parts[1])
		if err != nil {
			panic(err)
		}
		rules = append(rules, OrderRule{left, right})
	}

	printOrders := make([]PrintOrder, 0)

	for _, line := range lines[printOrderStartLine:] {
		printOrder := make(PrintOrder, 0)
		parts := strings.Split(line, ",")
		for _, part := range parts {
			num, err := strconv.Atoi(part)
			if err != nil {
				panic(err)
			}
			printOrder = append(printOrder, num)
		}
		printOrders = append(printOrders, printOrder)
	}

	return rules, printOrders
}

type CustomSortList struct {
	index map[int][]OrderRule
}

func (c *CustomSortList) Add(rule OrderRule) {
	if _, exists := c.index[rule.left]; !exists {
		c.index[rule.left] = make([]OrderRule, 0)
	}
	c.index[rule.left] = append(c.index[rule.left], rule)

	if _, exists := c.index[rule.right]; !exists {
		c.index[rule.right] = make([]OrderRule, 0)
	}
	c.index[rule.right] = append(c.index[rule.right], rule)

}

func (c *CustomSortList) PrintListIsValid(printOrder PrintOrder) bool {
	for i := 0; i < len(printOrder)-1; i++ {
		leftPrint := printOrder[i]
		rightPrint := printOrder[i+1]
		leftOrderRules, leftExists := c.index[leftPrint]
		if !leftExists {
			return false
		}

		found := false
		for _, leftOrderRule := range leftOrderRules {
			if leftOrderRule.right == rightPrint {
				found = true
				break
			}
		}
		if !found {
			return false
		}

	}
	return true
}

func (c *CustomSortList) Sort(printOrder PrintOrder) PrintOrder {
	printOrders := make(map[int]bool, len(printOrder))
	for _, num := range printOrder {
		printOrders[num] = true
	}

	slices.SortFunc(printOrder, func(i, j int) int {
		orderRules := c.index[i]
		for _, orderRule := range orderRules {
			if orderRule.left == j {
				return -1
			} else if orderRule.right == j {
				return 1
			}
		}
		return 0
	})

	return printOrder
}

func main() {
	rules, printOrders := parseInput(os.Args[1])

	listCustomSort := CustomSortList{make(map[int][]OrderRule)}

	for i := 0; i < len(rules); i++ {
		listCustomSort.Add(rules[i])
	}

	validPrintOrders := make([]PrintOrder, 0)
	invalidPrintOrders := make([]PrintOrder, 0)
	for _, printOrder := range printOrders {
		if listCustomSort.PrintListIsValid(printOrder) {
			validPrintOrders = append(validPrintOrders, printOrder)
		} else {
			invalidPrintOrders = append(invalidPrintOrders, printOrder)
		}
	}

	middleNumSum := 0
	for _, validPrintOrder := range validPrintOrders {
		middleNumSum += validPrintOrder[len(validPrintOrder)/2]
	}
	fmt.Println(middleNumSum)

	middleNumSum = 0
	for _, invalidPrintOrder := range invalidPrintOrders {
		sorted := listCustomSort.Sort(invalidPrintOrder)
		middleNumSum += sorted[len(sorted)/2]
	}
	fmt.Println(middleNumSum)
}
