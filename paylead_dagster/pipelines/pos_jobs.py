from dagster import repository, job, op

# Define a simple operation
@op
def hello_op():
    print("Hello Dagster!")

# Define a job using that op
@job
def hello_job():
    hello_op()

# Define the repository
@repository
def paylead_repo():
    return [hello_job]