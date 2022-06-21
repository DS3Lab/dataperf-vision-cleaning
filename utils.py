import pyarrow as pa

def fix(proposed_fixes, train, budget, gt_df):
    if len(proposed_fixes) > budget:
        raise ValueError("Submission takes more budget than expected, {}>{}".format(len(proposed_fixes), budget))
    fixed_points = train.take(proposed_fixes)
    fixed_points = fixed_points.to_pydict()
    train = train.to_pydict()
    # mutate labels
    # find the ground truth
    gt_labels = [gt_df[gt_df['ImageID'] == filename]['hv_label'].values[0] for filename in fixed_points['filename']]
    for row_id, each in enumerate(proposed_fixes):
        train['label'][each] = gt_labels[row_id]
    d = pa.Table.from_pydict(train)
    return d, len(proposed_fixes)