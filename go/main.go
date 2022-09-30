package main

import (
	"flag"
	"fmt"
	"io"
	"math/big"
	"os"
	"time"
)

var (
	ZERO  *big.Int = big.NewInt(0)
	ONE   *big.Int = big.NewInt(1)
	TWO   *big.Int = big.NewInt(2)
	THREE *big.Int = big.NewInt(3)

	PRINT_THRESHOLD = big.NewInt(WINDOW_SIZE)

	WINDOW_SIZE_BIG *big.Int = big.NewInt(WINDOW_SIZE)
	WINDOW_SIZE     int64    = 1000
)

var count = flag.Uint64("n", 10, "")
var store = flag.Bool("store", false, "if set to true, stores numbers and their stopping paths")

func main() {
	flag.Parse()

	if *store {
		if _, err := os.Stat("data.store"); os.IsNotExist(err) {
			_, err := os.Create("data.store")
			if err != nil {
				panic(err)
			}
		}

		go writer("data.store")
	}

	start := big.NewInt(0)
	elapsed := time.Now()

	out := make(chan string)

	go func(w io.Writer, elapsed time.Time, out chan string) {
		for r := range out {
			io.WriteString(w, r+fmt.Sprintf(" (%v elapsed)\n", time.Since(elapsed)))
		}
	}(os.Stdin, elapsed, out)

	var i uint64
	for ; i < *count; i++ {
		run_window(start, out, writer_chan)
	}
}

func run_window(start *big.Int, out chan string, writer_chan chan []byte) {
	tz := time.Now()

	window := new_window(start)
	start.Add(start, WINDOW_SIZE_BIG)

	for _, v := range window {
		go try_number(v, writer_chan)
	}

	if big.NewInt(0).Div(start, PRINT_THRESHOLD).Cmp(ZERO) > 0 {
		out <- fmt.Sprintf("tried window %v...%v in %v", start, big.NewInt(0).Add(start, WINDOW_SIZE_BIG), time.Since(tz))
		PRINT_THRESHOLD.Mul(PRINT_THRESHOLD, PRINT_THRESHOLD)
	}
}

func new_window(start *big.Int) []*big.Int {
	window := make([]*big.Int, 0, WINDOW_SIZE)
	for i := int64(0); i < WINDOW_SIZE; i++ {
		next := big.NewInt(0).Add(start, ONE)
		window = append(window, next)
	}

	return window
}

func try_number(n *big.Int, writer_chan chan []byte) uint64 {
	buf := []byte{}
	buf = append(buf, []byte(n.String())...)
	buf = append(buf, 'Y')

	var nSteps uint64
	for num := collatz(n); num.Cmp(ONE) != 0; num = collatz(n) {
		buf = append(buf, []byte(num.String())...)
		nSteps++
	}

	buf = append(buf, 'Z')
	writer_chan <- buf

	return nSteps
}

func collatz(n *big.Int) *big.Int {
	rmd := big.NewInt(0).Rem(n, TWO)
	if rmd.Cmp(ZERO) == 0 {
		return n.Div(n, TWO)
	} else if rmd.Cmp(ONE) == 0 {
		return n.Mul(n, THREE).Add(n, ONE)
	}

	return n
}

var writer_chan = make(chan []byte)

func writer(out string) {
	f, err := os.OpenFile(out, os.O_WRONLY, os.ModeAppend)
	if err != nil {
		panic("failed to open data file")
	}

	for req := range writer_chan {
		f.Write(req)
	}
}
