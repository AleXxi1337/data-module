def embeddings_filter(embeddings_json : dict, conditions : dict) -> list:
    valid_indices = set(range(len(embeddings_json['embeddings'])))

    for column, condition in conditions.items():
        
        column_values = embeddings_json[column]
        new_indices = []
        
        for idx in valid_indices:
            if column_values[idx] == condition:
                new_indices.append(idx)
        
        valid_indices = set(new_indices)
        
        if not valid_indices:
            break

    return [embeddings_json['embeddings'][idx] for idx in sorted(valid_indices)]