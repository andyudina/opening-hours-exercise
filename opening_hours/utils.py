def split_to_pairs(seq):
    """Split list into sublists with length == 2

    Args:
        seq (list): List to be split
 
    Returns:
        List of sublists with
    """
    size = 2
    return [seq[i:i + size] for i  in range(0, len(seq), size)]
