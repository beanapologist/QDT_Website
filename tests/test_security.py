import pytest
from src.security.qdt_security import (
    QDTSecurityCore,
    QDTAccessControl,
    validate_candidate,
    lucas_lehmer_small,
    verify_algorithm
)

def test_security_core():
    core = QDTSecurityCore()
    assert core.LAMBDA == 0.867
    assert core.GAMMA_D == 0.4497
    assert core.BETA == 0.310
    assert core.ETA == 0.520
    assert core.PHI == 1.618033
    assert core.PRIME_SEED == 244191827

def test_security_hash():
    core = QDTSecurityCore()
    hash_value = core._generate_security_hash()
    assert isinstance(hash_value, str)
    assert len(hash_value) == 64  # SHA-256 hash length

def test_access_control():
    core = QDTSecurityCore()
    access = QDTAccessControl(core)
    
    # Test public access
    assert access.authenticate_user("0", "0") == access.access_levels['PUBLIC']
    
    # Test prime hunter access
    assert access.authenticate_user("12345", "244191827") == access.access_levels['PRIME_HUNTER']

def test_validate_candidate():
    result = validate_candidate()
    assert result['matches_target']
    assert result['is_prime']

def test_lucas_lehmer():
    # Test known Mersenne primes
    assert lucas_lehmer_small(2)
    assert lucas_lehmer_small(3)
    assert lucas_lehmer_small(5)
    assert lucas_lehmer_small(7)
    
    # Test composite numbers
    assert not lucas_lehmer_small(4)
    assert not lucas_lehmer_small(6)

def test_verify_algorithm():
    results = verify_algorithm()
    assert len(results) == 7  # Number of test cases
    assert all("PRIME" in result for result in results)  # All should be prime 