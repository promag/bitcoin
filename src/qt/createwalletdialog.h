// Copyright (c) 2019 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BITCOIN_QT_CREATEWALLETDIALOGG_H
#define BITCOIN_QT_CREATEWALLETDIALOGG_H

#include <QDialog>

namespace Ui {
    class CreateWalletDialog;
}

/** Dialog for creating wallets
 */
class CreateWalletDialog : public QDialog
{
    Q_OBJECT

public:
    explicit CreateWalletDialog(QWidget* parent);
    ~CreateWalletDialog();

    QString getWalletName() const;
    bool isBlank() const;
    bool isDisabledPrivateKeys() const;
    bool isEncrypt() const;

private:
    Ui::CreateWalletDialog *ui;
};

#endif // BITCOIN_QT_CREATEWALLETDIALOGG_H
