package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func Must[T any](r T, err error) T {
	if err != nil {
		panic(err)
	}
	return r
}

type PacketVersion int
type PacketTypeID int
type PacketOperationLabel int

const (
	PacketVersionBits   PacketVersion        = 3
	PacketTypeBits      PacketTypeID         = 3
	PacketOperationBits PacketOperationLabel = 1
	PacketTypeLiteral   PacketTypeID         = 4
)

type LiteralPacket struct {
	Version PacketVersion
	Type    PacketTypeID
	Value   string
}

type OperationPacket struct {
	Version             PacketVersion
	Type                PacketTypeID
	Operation           PacketOperationLabel
	TotalSubPacketsBits int
	SubPackets          []interface{} // Can contain both LiteralPacket and OperationPacket
}

const (
	LiteralPacketType   = "literal"
	OperationPacketType = "operation"
)

func ParseInput(input string, bits int) (string, string, error) {
	if len(input) < bits {
		return "", "", fmt.Errorf("not enough bits to parse, expected %d more bits", bits-len(input))
	}
	return input[:bits], input[bits:], nil
}

func PacketType(input string) (string, error) {
	necessaryBits := int(PacketVersionBits) + int(PacketTypeBits)
	if len(input) < necessaryBits {
		return "", fmt.Errorf("not enough bits to parse packet type")
	}
	packetTypeBits := input[PacketVersionBits:necessaryBits]
	packetType, err := strconv.ParseInt(packetTypeBits, 2, 32)
	if err != nil {
		return "", fmt.Errorf("failed to parse packet type: %w", err)
	}
	switch int(packetType) {
	case int(PacketTypeLiteral):
		return LiteralPacketType, nil
	default:
		return OperationPacketType, nil
	}
}

func ParsePacket(input string) (interface{}, string, error) {
	if StopParsing(input) {
		return nil, input, nil
	}

	packetType, err := PacketType(input)
	if err != nil {
		return nil, "", err
	}

	switch packetType {
	case LiteralPacketType:
		return NewLiteralPacket(input)
	case OperationPacketType:
		return NewOperationPacket(input)
	default:
		return nil, "", fmt.Errorf("unknown packet type: %s", packetType)
	}
}

func NewLiteralPacket(input string) (*LiteralPacket, string, error) {
	packet := &LiteralPacket{}
	var err error

	var versionBits string
	versionBits, input, err = ParseInput(input, int(PacketVersionBits))
	if err != nil {
		return nil, "", err
	}

	version, err := strconv.ParseInt(versionBits, 2, 32)
	if err != nil {
		return nil, "", fmt.Errorf("failed to parse version bits: %w", err)
	}
	packet.Version = PacketVersion(version)

	var typeBits string
	typeBits, input, err = ParseInput(input, int(PacketTypeBits))
	if err != nil {
		return nil, "", err
	}

	parsedType, err := strconv.ParseInt(typeBits, 2, 32)
	if err != nil {
		return nil, "", fmt.Errorf("failed to parse type bits: %w", err)
	}
	packet.Type = PacketTypeID(parsedType)

	if len(input) < 5 {
		return nil, "", fmt.Errorf("not enough bits to parse value")
	}
	if len(input) < 5 {
		packet.Value = "0"
		return packet, input, nil
	}

	valueBits := ""
	lastGroup := false
	for {
		if len(input) < 5 {
			log.Println("added right padding")
			input += strings.Repeat("0", 5-len(input))
		}
		group := input[:5]
		lastGroup = group[0] == '0'
		valueBits += group[1:5]
		input = input[5:]
		if lastGroup {
			break
		}
	}
	parsedValue, err := strconv.ParseInt(valueBits, 2, 64)
	packet.Value = strconv.Itoa(int(parsedValue))

	if err != nil {
		return nil, "", fmt.Errorf("failed to parse value bits: %w", err)
	}
	return packet, input, nil
}

func NewOperationPacket(input string) (*OperationPacket, string, error) {
	packet := &OperationPacket{}
	var err error

	var versionBits string
	versionBits, input, err = ParseInput(input, int(PacketVersionBits))
	if err != nil {
		return nil, "", err
	}

	version, err := strconv.ParseInt(versionBits, 2, 32)
	if err != nil {
		return nil, "", fmt.Errorf("failed to parse version bits: %w", err)
	}
	packet.Version = PacketVersion(version)

	var typeBits string
	typeBits, input, err = ParseInput(input, int(PacketTypeBits))
	if err != nil {
		return nil, "", err
	}

	parsedType, err := strconv.ParseInt(typeBits, 2, 32)
	if err != nil {
		return nil, "", fmt.Errorf("failed to parse type bits: %w", err)
	}
	packet.Type = PacketTypeID(parsedType)

	if len(input) < 1 {
		return nil, "", fmt.Errorf("not enough bits to parse operation")
	}
	operationBits, input, err := ParseInput(input, int(PacketOperationBits))
	if err != nil {
		return nil, "", err
	}

	operation, err := strconv.ParseInt(operationBits, 2, 32)
	if err != nil {
		return nil, "", fmt.Errorf("failed to parse operation bits: %w", err)
	}
	packet.Operation = PacketOperationLabel(operation)

	var totalSubPacketsBits string
	nextNBits := 0
	if packet.Operation == 0 {
		nextNBits = 15
	} else {
		nextNBits = 11
	}

	totalSubPacketsBits, input, err = ParseInput(input, nextNBits)
	if err != nil {
		return nil, "", err
	}

	totalBits, err := strconv.ParseInt(totalSubPacketsBits, 2, 32)
	if err != nil {
		return nil, "", fmt.Errorf("failed to parse total sub-packets bits: %w", err)
	}
	packet.TotalSubPacketsBits = int(totalBits)

	// Parse subpackets based on operation type
	if packet.Operation == 0 {
		// Length-based: Parse packets until we've consumed TotalSubPacketsBits
		subPacketInput := input[:packet.TotalSubPacketsBits]
		input = input[packet.TotalSubPacketsBits:]

		for len(subPacketInput) > 0 && !StopParsing(subPacketInput) {
			subPacket, remaining, err := ParsePacket(subPacketInput)
			if err != nil {
				return nil, "", err
			}
			if subPacket == nil {
				break
			}
			packet.SubPackets = append(packet.SubPackets, subPacket)
			subPacketInput = remaining
		}
	} else {
		// Count-based: Parse exactly TotalSubPacketsBits number of packets
		for i := 0; i < packet.TotalSubPacketsBits; i++ {
			subPacket, remaining, err := ParsePacket(input)
			if err != nil {
				return nil, "", err
			}
			if subPacket == nil {
				break
			}
			packet.SubPackets = append(packet.SubPackets, subPacket)
			input = remaining
		}
	}

	return packet, input, nil
}

func (p *LiteralPacket) String() string {
	return fmt.Sprintf("LiteralPacket{Version: %d, Type: %d, Value: %s}", p.Version, p.Type, p.Value)
}

func (p *OperationPacket) String() string {
	base := fmt.Sprintf("OperationPacket{Version: %d, Type: %d, Operation: %d, TotalSubPackets: %d}", p.Version, p.Type, p.Operation, p.TotalSubPacketsBits)
	for _, subPacket := range p.SubPackets {
		base += fmt.Sprintf("\n\t%v", subPacket)
	}
	return base
}

func ReadInput(filename string) string {
	return string(Must(os.ReadFile(filename)))
}

func HexToBinary(hex string) string {
	result := ""
	for _, c := range hex {
		ui := Must(strconv.ParseUint(string(c), 16, 64))
		result += fmt.Sprintf("%04b", ui)
	}
	return result
}

func StopParsing(input string) bool {
	if len(input) < 5 {
		return true
	}
	for _, c := range input {
		if c != '0' {
			return false
		}
	}
	return true
}

// part 1

func VersionSum(packets []interface{}) int {
	sum := 0
	for _, packet := range packets {
		switch p := packet.(type) {
		case *LiteralPacket:
			sum += int(p.Version)
		case *OperationPacket:
			sum += int(p.Version)
			sum += VersionSum(p.SubPackets)
		}
	}
	return sum

}

// part 2
func Sum(packets []interface{}) int {
	sum := 0
	for _, packet := range packets {
		sum += Calculate(packet)
	}
	return sum
}

func Product(packets []interface{}) int {
	product := 1
	for _, packet := range packets {
		product *= Calculate(packet)
	}
	return product
}

func Min(packets []interface{}) int {
	if len(packets) == 0 {
		return 0
	}
	min := Calculate(packets[0])
	for _, packet := range packets[1:] {
		value := Calculate(packet)
		if value < min {
			min = value
		}
	}
	return min
}

func Max(packets []interface{}) int {
	if len(packets) == 0 {
		return 0
	}
	max := Calculate(packets[0])
	for _, packet := range packets[1:] {
		value := Calculate(packet)
		if value > max {
			max = value
		}
	}
	return max
}

func GreaterThan(packets []interface{}) int {
	if len(packets) < 2 {
		return 0
	}
	if Calculate(packets[0]) > Calculate(packets[1]) {
		return 1
	}
	return 0
}

func LessThan(packets []interface{}) int {
	if len(packets) < 2 {
		return 0
	}
	if Calculate(packets[0]) < Calculate(packets[1]) {
		return 1
	}
	return 0
}

func EqualTo(packets []interface{}) int {
	if len(packets) < 2 {
		return 0
	}
	if Calculate(packets[0]) == Calculate(packets[1]) {
		return 1
	}
	return 0
}

func Calculate(packet interface{}) int {
	switch p := packet.(type) {
	case *LiteralPacket:
		return Must(strconv.Atoi(p.Value))
	case *OperationPacket:
		switch p.Type {
		case 0: // Sum
			return Sum(p.SubPackets)
		case 1: // Product
			return Product(p.SubPackets)
		case 2: // Minimum
			return Min(p.SubPackets)
		case 3: // Maximum
			return Max(p.SubPackets)
		case 5: // Greater than
			return GreaterThan(p.SubPackets)
		case 6: // Less than
			return LessThan(p.SubPackets)
		case 7: // Equal to
			return EqualTo(p.SubPackets)
		default:
			log.Fatalf("unknown operation type: %d", p.Type)
			return 0
		}
	default:
		log.Fatalf("unknown packet type: %T", packet)
		return 0
	}
}
func main() {
	input := ReadInput("input.txt")
	input = HexToBinary(input)
	var packets []interface{}

	for !StopParsing(input) {
		packet, remaining, err := ParsePacket(input)
		if err != nil {
			log.Fatal(err)
		}
		if packet == nil {
			break
		}
		packets = append(packets, packet)
		input = remaining
	}

	for _, packet := range packets {
		fmt.Println(packet)
	}

	fmt.Println("Version sum:", VersionSum(packets))
	fmt.Println("Calculation result:", Sum(packets))
}
