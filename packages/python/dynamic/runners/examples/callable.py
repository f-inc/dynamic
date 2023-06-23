from dynamic.runners.callable import CallableRunner, CallableRunnerConfig

if __name__ == "__main__":
    print("Testing class...")

    def hello(msg):
        return msg
    
    config = CallableRunnerConfig(params=dict(msg="Hello World!\n-from Runner"))

    runner = CallableRunner(hello, config)

    print("Runner created and running...")
    print(runner.run())