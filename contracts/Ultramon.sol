// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.27;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721URIStorage} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract Ultramon is ERC721, ERC721URIStorage, Ownable {
    struct Ultramon {
        string _name;
        string _type;
        uint256 _hp;
        uint256 _pc;
        uint256 _d;
        bool _shiny;
    }

    struct Entry {
        string _name;
        string _type;
    }

    Entry[] private _entries;
    uint256 private _nextTokenId;
    mapping (uint256 _tokenID => Ultramon _ultramon) public ultramons;

    constructor(address initialOwner)
        ERC721("Ultramon", "ULTRA")
        Ownable(initialOwner)
    {
        _entries.push(
            Entry({ _name: "Charizard", _type: "Fuego" })
        );
        _entries.push(
            Entry({ _name: "Pikachu", _type: "Electrico" })
        );
    }

    function _createUltramon(
        uint256 _tokenId
    ) private {
        Entry memory entry = _entries[block.timestamp % 2];
        Ultramon memory ultramon = Ultramon({
            _name: entry._name,
            _type: entry._type,
            _hp: block.timestamp % 30,
            _pc: block.timestamp % 15,
            _d: block.timestamp % 10,
            _shiny: (block.timestamp % 1000) > 950
        });
        ultramons[_tokenId] = ultramon;
    }

    function safeMint(address to)
        public
        onlyOwner
        returns (uint256)
    {
        uint256 tokenId = _nextTokenId;
        _nextTokenId++;
        _safeMint(to, tokenId);
        _createUltramon(tokenId);
        return tokenId;
    }

    // The following functions are overrides required by Solidity.

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}