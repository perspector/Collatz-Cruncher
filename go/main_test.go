package main

import (
	"math/big"
	"testing"
)

func TestCollatz(t *testing.T) {
	r := big.NewInt(10)
	if collatz(r).Cmp(big.NewInt(5)) != 0 {
		t.Fail()
	}

	r = big.NewInt(11)
	if collatz(r).Cmp(big.NewInt(34)) != 0 {
		t.Fail()
	}
}

func BenchmarkCollatz(b *testing.B) {
	r := big.NewInt(10)
	if collatz(r).Cmp(big.NewInt(5)) != 0 {
		b.Fail()
	}

	r = big.NewInt(11)
	if collatz(r).Cmp(big.NewInt(34)) != 0 {
		b.Fail()
	}
}
