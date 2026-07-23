import argparse
import sys

from pyvault import Category
from pyvault.storage import BankStorage

DATA_FILE = "data.json"


def build_parser():
    parser = argparse.ArgumentParser(description="PyVault: a simple personal finance tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("owner")
    create.add_argument("--balance", type=float, default=0.0)

    deposit = subparsers.add_parser("deposit")
    deposit.add_argument("owner")
    deposit.add_argument("amount", type=float)
    deposit.add_argument("--category", default="other", choices=[c.value for c in Category])
    deposit.add_argument("--note", default="")

    withdraw = subparsers.add_parser("withdraw")
    withdraw.add_argument("owner")
    withdraw.add_argument("amount", type=float)
    withdraw.add_argument("--category", default="other", choices=[c.value for c in Category])
    withdraw.add_argument("--note", default="")

    transfer = subparsers.add_parser("transfer")
    transfer.add_argument("sender")
    transfer.add_argument("recipient")
    transfer.add_argument("amount", type=float)
    transfer.add_argument("--note", default="")

    balance = subparsers.add_parser("balance")
    balance.add_argument("owner")

    summary = subparsers.add_parser("summary")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    with BankStorage(DATA_FILE) as bank:
        if args.command == "create":
            bank.create_account(args.owner, args.balance)
            print(f"Created account for {args.owner} with balance {args.balance:.2f}")

        elif args.command == "deposit":
            account = bank.get_account(args.owner)
            account.deposit(args.amount, category=Category(args.category), note=args.note)
            print(f"Deposited {args.amount:.2f} to {args.owner}. New balance: {account.balance:.2f}")

        elif args.command == "withdraw":
            account = bank.get_account(args.owner)
            account.withdraw(args.amount, category=Category(args.category), note=args.note)
            print(f"Withdrew {args.amount:.2f} from {args.owner}. New balance: {account.balance:.2f}")

        elif args.command == "transfer":
            bank.transfer(args.sender, args.recipient, args.amount, note=args.note)
            print(f"Transferred {args.amount:.2f} from {args.sender} to {args.recipient}")

        elif args.command == "balance":
            account = bank.get_account(args.owner)
            print(f"{args.owner}'s balance: {account.balance:.2f}")

        elif args.command == "summary":
            for account in bank:
                print(f"{account.owner:15s} {account.balance:>10.2f}")
            print(f"{'TOTAL':15s} {bank.total_balance():>10.2f}")


if __name__ == "__main__":
    main()