import torch



def find_slots_from(sentence, model, x_tokenizer, y_tokenizer, device, max_len=45):
    model.eval()
    sentence = sentence.strip().split(" ")
    sentence = ["<sos>"] + sentence + ["<eos>"]
    src_indexes = x_tokenizer.words_to_seq(sentence)
    print("source lenght : ", len(src_indexes), src_indexes)
    src_tensor = torch.LongTensor(src_indexes).unsqueeze(0).to(device)
    with torch.no_grad():
        encoder_conved, encoder_combined = model.encoder(src_tensor)
    trg_indexes = [y_tokenizer.word_to_index["<sos>"]]
    for i in range(max_len):
        trg_tensor = torch.LongTensor(trg_indexes).unsqueeze(0).to(device)
        # print("trg_tensor", trg_tensor.size())
        with torch.no_grad():
            output, attention = model.decoder(trg_tensor, encoder_conved, encoder_combined)
        # print("output", output.size())
        # print("output.argmax(2)", output.argmax(2).size())
        pred_token = output.argmax(2)[:,-1].item()
        trg_indexes.append(pred_token)
        # print("کلمه: ", x_tokenizer.seq_to_words([src_indexes[i]]), "اسلات: ", y_tokenizer.seq_to_words([pred_token]))

        if pred_token == y_tokenizer.word_to_index["<eos>"]:
            break
    trg_tokens = y_tokenizer.seq_to_words(trg_indexes)
    return trg_tokens[1:], attention