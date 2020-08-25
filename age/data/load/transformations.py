import pandas as pd


def add_both_sexes(data: pd.DataFrame) -> pd.DataFrame:
    """Add male and female data to obtain data for both sexes combined."""
    if len(data.Sex.unique()) != 2:
        raise ValueError(
            f'Expecting 2 sexes in data.Sex, but found {len(data.Sex.unique())}')
    both = data.groupby(['Date', 'Age']).sum().reset_index().copy()
    both['Sex'] = 'b'
    return pd.concat([data, both], axis=0)


def rescale(data: pd.DataFrame, ref_data: pd.DataFrame, field: str) -> pd.DataFrame:
    """Proportionally rescale data so that totals match daily totals given in ref_data"""
    scale = data.query('Sex == "b"').groupby('Date').sum().merge(
        ref_data[['DATE', field]], left_on='Date', right_on='DATE')
    scale['factor'] = scale[f'{field}_y'] / scale[f'{field}_x']
    # Don't rescale small values
    scale.loc[scale[f'{field}_y'] < 10, 'factor'] = 1
    data = data.merge(scale[['DATE', 'factor']],
                      left_on='Date', right_on='DATE')
    data[field] = round(data[field] * data.factor)
    data = data.drop(['DATE', 'factor'], axis='columns')
    return data


def periodic_to_daily(data: pd.DataFrame) -> pd.DataFrame:
    """Convert a dataframe that has new cases or deaths sampled periodically to daily sampling."""
    process_df = data.set_index(['Date', 'Age', 'Sex']).unstack().unstack().fillna(0).reset_index()
    
    gap_days = process_df.Date.diff().dt.days
    gap_days.index = process_df.Date
    
    process_df = process_df.set_index('Date').divide(gap_days, axis=0)
    process_df = process_df.resample('d').interpolate()
    process_df = round(process_df.stack().stack().reset_index())
    
    return process_df


def smooth_sample(data: pd.DataFrame, rolling_window: int = 3) -> pd.DataFrame:
    """Apply smoothing to a sample of data."""
    return round(
        data.set_index(['Date', 'Age', 'Sex'])
        .unstack().unstack().fillna(0.)
        .rolling(rolling_window, center=True, min_periods=1)
        .mean()).stack().stack().reset_index()


def cumulative_to_new(data: pd.DataFrame) -> pd.DataFrame:
    """Convert a time series of cumulative counts in tidy format to a one that of daily counts."""
    return (data
            .set_index(['Date', 'Age', 'Sex'])
            .unstack()
            .unstack()
            .diff()
            .stack()
            .stack()
            .reset_index())


def ensure_contiguous(data):
    """Ensure the dates are contiguous in the given data."""
    data = data.drop_duplicates(['Date', 'Sex', 'Age'])
    data = data.set_index(['Date', 'Sex', 'Age']).unstack().unstack()
    data = data.fillna(0)  # Fill the holes in the age-sex cross product
    data = data.resample('d').ffill()  # Fill the holes in the dates
    return data.stack().stack().reset_index()
