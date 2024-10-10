import pandas as pd

def test_pandas():
    try:
        data = {'Name': ['Alice', 'Bob', 'Charlie'],
                'Age': [25, 30, 35]}
        df = pd.DataFrame(data)

        print("DataFrame created successfully:")
        print(df)

        print(f"\nUsing pandas version: {pd.__version__}")

        return True

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    if test_pandas():
        print("\nPandas is working correctly!")
    else:
        print("\nThere was an issue with pandas.")