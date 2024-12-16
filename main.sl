U8* msg = "Hello, world!";
I32 value = 0;    
loop {
    if value == 5 {
        break;
    }
    print("%s", msg);
    inc(value);
}
end(0);